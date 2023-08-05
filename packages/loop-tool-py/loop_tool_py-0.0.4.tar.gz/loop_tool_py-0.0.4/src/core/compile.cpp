/*
Copyright (c) Facebook, Inc. and its affiliates.

This source code is licensed under the MIT license found in the
LICENSE file in the root directory of this source tree.
*/
#include "compile.h"
#include "backend.h"
#include "error.h"
#include <algorithm>
#include <chrono>
#include <cstring>
#include <iostream>
#include <unordered_set>

InnerFnType gen_fn(const LoopTree &lt, const Auxiliary &aux,
                   LoopTree::TreeRef ref);

// Return LCA of node and it's users
LoopTree::TreeRef get_scope(const LoopTree &lt, LoopTree::TreeRef ref) {
  ASSERT(lt.node(ref).kind == LoopTree::NODE);
  const auto &node = lt.ir.node(lt.node(ref).node);

  // find all usage of this value
  std::unordered_set<IR::NodeRef> users = {node.outputs().begin(),
                                           node.outputs().end()};
  std::vector<LoopTree::TreeRef> uses;
  lt.walk([&](LoopTree::TreeRef tr, int) {
    if (lt.node(tr).kind == LoopTree::NODE) {
      if (users.count(lt.node(tr).node)) {
        uses.emplace_back(tr);
      }
    }
  });
  ASSERT(users.size() == uses.size());

  // find least common ancestor
  auto ancestor = lt.parent(ref);
  if (node.op() == "write") {
    ancestor = -1;
  } else {
    for (auto use : uses) {
      ancestor = lt.lca(lt.lca(ref, use), ancestor);
    }
  }

  return ancestor;
}

// check if there are reductions in the body of this tree
// over the variable
bool trivially_parallel(const LoopTree &lt, LoopTree::TreeRef ref) {
  bool threadable = true;
  auto tree_v = lt.node(ref).loop.var;
  lt.walk(
      [&](LoopTree::TreeRef ref, int) {
        if (lt.node(ref).kind == LoopTree::LOOP) {
          return;
        }
        auto node_ref = lt.node(ref).node;
        bool iters_over = false;
        for (auto v : lt.ir.all_vars(node_ref)) {
          if (v == tree_v) {
            iters_over = true;
            break;
          }
        }
        if (iters_over) {
          bool pointwise = false;
          for (auto v : lt.ir.pointwise_vars(node_ref)) {
            if (v == tree_v) {
              pointwise = true;
            }
          }
          if (!pointwise) {
            threadable = false;
          }
        }
      },
      ref);
  return threadable;
}

/*
Nodes are values! Here's how memory is allocated:
1. Immediately deduce their scope - find LCA among dependents
2. Preserving the node's var order, find the minimum required memory to allocate
  for c:
    for a in 3r1: // shared scope
      for b in 2:
        for a in 5:
          create(T[a,b,c])
      for b in 2:
        for a in 5:
          for k: // note this is unrelated
            use(T[a,b,c])
  T[a, b, c], scope is {a:{5,0}, {b:{2,0}}, which means we need to allocate
       10 elements (scope for C and part of A is shared).  Even though
       A is a total of 16 elems, we can allocate 5 elems in the shared scope!
       We will partially use this allocation in the tail run (1/5th of it)
  We can also handle "weird" splits:
  for c:
    for a in 3r1: // shared scope
      for b in 2:
        for a in 2r1: // note the loops no longer match and theres a tail
          for a in 2:
            create(T[a,b,c])
      for b in 2:
        for a in 5:
          for k:
            use(T[a,b,c])
  Because we have strong invariants, we know that the LCA preserves sizing
  despite complex loop tiling.  we still have 5 a elems and 2 b elems for a
total of 10 The resultant expressions will share memory but will have different
  indexing semantics, which allows us to chain unique strategies without concern
  of accidental memory over-use

  gen_alloc maps a node to its LCA, size, idx into allocation map
  gen_idx_vec maps a user + alloc to an indexing vector
*/

void gen_alloc(const LoopTree &lt, Auxiliary &aux, LoopTree::TreeRef ref) {
  ASSERT(lt.node(ref).kind == LoopTree::NODE);
  LoopTree::TreeRef lca = get_scope(lt, ref);

  // var -> running size, last tail
  auto loop_ref = lt.parent(ref);
  auto var_vec = lt.ir.node(lt.node(ref).node).vars();
  std::unordered_set<IR::VarRef> vars = {var_vec.begin(), var_vec.end()};
  std::unordered_map<IR::VarRef, std::pair<int, int>> var_sizes;
  while (loop_ref != lca) {
    auto loop = lt.node(loop_ref).loop;
    auto size = loop.size;
    if (!vars.count(loop.var)) {
      loop_ref = lt.parent(loop_ref);
      continue;
    }
    if (var_sizes.count(loop.var)) {
      auto s = var_sizes[loop.var];
      size = size * (s.first + s.second);
    }
    var_sizes[loop.var] = std::make_pair(size, loop.tail);
    loop_ref = lt.parent(loop_ref);
  }

  size_t total = 1;
  for (auto &p : var_sizes) {
    total *= (p.second.first + p.second.second);
  }
  auto node_ref = lt.node(ref).node;
  bool reduction = (lt.ir.pointwise_vars(node_ref).size() !=
                    lt.ir.all_vars(node_ref).size());
  bool should_init = false;
  float init_val = -1337;
  if (lt.ir.node(node_ref).op() == "mul") {
    should_init = reduction;
    init_val = 1;
  } else if (lt.ir.node(node_ref).op() == "add") {
    should_init = reduction;
    init_val = 0;
  }

  Allocation alloc{total,       static_cast<int>(aux.allocs.size()),
                   should_init, init_val,
                   lca,         ref};
  aux.allocs[node_ref] = alloc;
  aux.resets[alloc.lca].emplace_back(alloc);
}

std::vector<std::pair<int, size_t>> gen_idx_vector(const LoopTree &lt,
                                                   const Allocation &alloc,
                                                   LoopTree::TreeRef use) {
  std::vector<std::pair<int, size_t>> idx_vec;

  // get index of loop into indices[MAX_DEPTH]
  // by counting number of parents
  auto loop_ref = lt.parent(use);
  if (loop_ref == -1) {
    return idx_vec;
  }
  auto idx = 0;
  auto size = 1;
  auto depth = lt.node(loop_ref).depth;

  auto vs = lt.ir.node(lt.node(alloc.producer).node).vars();
  std::unordered_set<IR::VarRef> vars = {vs.begin(), vs.end()};

  // first we collect the orders of each var
  std::unordered_map<IR::VarRef, std::vector<LoopTree::TreeRef>> var_loops;
  while (loop_ref != alloc.lca) {
    auto loop = lt.node(loop_ref).loop;
    if (vars.count(loop.var)) {
      var_loops[loop.var].emplace_back(loop_ref);
    }
    loop_ref = lt.parent(loop_ref);
  }
  std::reverse(vs.begin(), vs.end());
  for (const auto &v : vs) {
    auto inner_size = size; // size of all inner vars
    for (auto l : var_loops[v]) {
      auto idx = lt.node(l).depth;
      idx_vec.emplace_back(std::make_pair(idx, size));
      auto loop = lt.node(l).loop;
      size = loop.size * size + loop.tail * inner_size;
    }
  }
  return idx_vec;
}

/*
 an index function maps a point in memory given a location in the loop tree
*/
std::function<size_t(int[MAX_DEPTH])> gen_idx_func(const LoopTree &lt,
                                                   const Allocation &alloc,
                                                   LoopTree::TreeRef use) {
  auto ref = alloc.producer;
  ASSERT(lt.node(ref).kind == LoopTree::NODE);
  ASSERT(lt.node(use).kind == LoopTree::NODE);

  auto idx_vec = gen_idx_vector(lt, alloc, use);
  // if (lt.ir.node(lt.node(ref).node).vars().size() > 2) {
  //  std::cerr << "vec for alloc "<<lt.ir.dump(lt.node(ref).node)<<" ";
  //  for (auto i : idx_vec) {
  //    std::cerr << i.first << "->" << i.second << ", ";
  //  }
  //  std::cerr << "\n";
  //}
  return [=](int indices[MAX_DEPTH]) {
    size_t idx = 0;
    for (const auto &p : idx_vec) {
      idx += indices[p.first] * p.second;
    }
    return idx;
  };
}

InnerFnType gen_read(const LoopTree &lt, LoopTree::TreeRef ref,
                     const Allocation &alloc) {
  int external_memory = -1;
  for (auto i = 0; i < lt.ir.inputs().size(); ++i) {
    if (lt.ir.inputs()[i] == lt.node(ref).node) {
      external_memory = i;
    }
  }
  ASSERT(external_memory > -1 && "No input found!");

  auto idx_fn = gen_idx_func(lt, alloc, ref);
  auto alloc_read = alloc;
  // TODO this is a hacky way to ensure all variables are in the indexing
  alloc_read.lca = -1;
  auto read_idx_fn = gen_idx_func(lt, alloc_read, ref);
  auto inp_memory = alloc.idx + lt.ir.inputs().size() + lt.ir.outputs().size();

  return [=](const std::vector<void *> &memory, int indices[MAX_DEPTH],
             int tails[MAX_DEPTH]) {
    for (auto i = 0; i < MAX_DEPTH; ++i) {
      if (tails[i]) {
        return;
      }
    }
    ((float *)memory[inp_memory])[idx_fn(indices)] =
        ((float *)memory[external_memory])[read_idx_fn(indices)];
  };
}

InnerFnType gen_write(const LoopTree &lt,
                      const std::unordered_map<IR::NodeRef, Allocation> &allocs,
                      LoopTree::TreeRef ref) {
  int external_memory = -1;
  auto tree_node = lt.node(ref);
  for (auto i = 0; i < lt.ir.outputs().size(); ++i) {
    if (lt.ir.outputs()[i] == tree_node.node) {
      external_memory = i + lt.ir.inputs().size();
    }
  }
  ASSERT(external_memory > -1 && "No output found!");

  const auto &n = lt.ir.node(tree_node.node);
  ASSERT(n.inputs().size() == 1);
  ASSERT(n.outputs().size() == 0);

  auto inp = n.inputs()[0];

  auto inp_idx_fn = gen_idx_func(lt, allocs.at(inp), ref);
  auto out_idx_fn = gen_idx_func(lt, allocs.at(tree_node.node), ref);
  auto alloc = allocs.at(tree_node.node);
  auto input_memory =
      allocs.at(inp).idx + lt.ir.inputs().size() + lt.ir.outputs().size();

  return [=](const std::vector<void *> &memory, int indices[MAX_DEPTH],
             int tails[MAX_DEPTH]) {
    for (auto i = 0; i < MAX_DEPTH; ++i) {
      if (tails[i]) {
        return;
      }
    }
    ((float *)memory[external_memory])[out_idx_fn(indices)] =
        ((float *)memory[input_memory])[inp_idx_fn(indices)];
    // std::cerr << "RWITIGN " << ((float
    // *)memory[external_memory])[out_idx_fn(indices)] <<"\n";
  };
}

InnerFnType gen_add(const LoopTree &lt,
                    const std::unordered_map<IR::NodeRef, Allocation> &allocs,
                    LoopTree::TreeRef ref) {
  auto tree_node = lt.node(ref);
  const auto &n = lt.ir.node(tree_node.node);

  std::vector<std::pair<std::function<size_t(int[MAX_DEPTH])>, int>> inputs;
  std::pair<std::function<size_t(int[MAX_DEPTH])>, int> output;

  auto mem_off = lt.ir.inputs().size() + lt.ir.outputs().size();
  for (auto &inp_ref : n.inputs()) {
    const auto &alloc = allocs.at(inp_ref);
    inputs.emplace_back(gen_idx_func(lt, alloc, ref), alloc.idx + mem_off);
  }
  auto out_alloc = allocs.at(tree_node.node);

  output =
      std::make_pair(gen_idx_func(lt, out_alloc, ref), out_alloc.idx + mem_off);
  return [=](const std::vector<void *> &memory, int indices[MAX_DEPTH],
             int tails[MAX_DEPTH]) {
    for (auto i = 0; i < MAX_DEPTH; ++i) {
      if (tails[i]) {
        return;
      }
    }
    for (auto inp : inputs) {
      // std::cerr << "adding to " << output.second << "[" <<
      // output.first(indices) << "]" << " from "
      //  << inp.second << "[" << inp.first(indices) << "]\n";
      //   std::cerr << "adding " <<
      //     ((float *)memory[output.second])[output.first(indices)] << " < " <<
      //     ((float *)memory[inp.second])[inp.first(indices)] << "\n";
      ((float *)memory[output.second])[output.first(indices)] +=
          ((float *)memory[inp.second])[inp.first(indices)];
    }
  };
};

InnerFnType gen_mul(const LoopTree &lt,
                    const std::unordered_map<IR::NodeRef, Allocation> &allocs,
                    LoopTree::TreeRef ref) {
  auto tree_node = lt.node(ref);
  const auto &n = lt.ir.node(tree_node.node);

  std::vector<std::pair<std::function<size_t(int[MAX_DEPTH])>, int>> inputs;
  std::pair<std::function<size_t(int[MAX_DEPTH])>, int> output;

  auto mem_off = lt.ir.inputs().size() + lt.ir.outputs().size();
  for (auto &inp_ref : n.inputs()) {
    const auto &alloc = allocs.at(inp_ref);
    inputs.emplace_back(gen_idx_func(lt, alloc, ref), alloc.idx + mem_off);
  }
  auto out_alloc = allocs.at(tree_node.node);

  output =
      std::make_pair(gen_idx_func(lt, out_alloc, ref), out_alloc.idx + mem_off);
  auto depth = lt.node(ref).depth;
  return [=](const std::vector<void *> &memory, int indices[MAX_DEPTH],
             int tails[MAX_DEPTH]) {
    for (auto i = 0; i < MAX_DEPTH; ++i) {
      if (tails[i]) {
        return;
      }
    }
    // std::cerr << "incidices: ";
    // for (auto i = 0; i < depth; ++i) {
    // std::cerr << indices[i] << ", ";
    //}
    // std::cerr << "\n";
    for (auto inp : inputs) {
      // std::cerr << output.first(indices) << " muled by " <<
      // inp.first(indices) << "\n"; std::cerr << "muling to " << output.second
      // << "[" << output.first(indices) << "]" << " from "
      //  << inp.second << "[" << inp.first(indices) << "]\n";
      // std::cerr << "mul " <<
      //((float *)memory[output.second])[output.first(indices)] << " *= " <<
      //    ((float *)memory[inp.second])[inp.first(indices)] <<"\n";
      ((float *)memory[output.second])[output.first(indices)] *=
          ((float *)memory[inp.second])[inp.first(indices)];
    }
  };
};

InnerFnType gen_leaf(const LoopTree &lt, const Auxiliary &aux,
                     LoopTree::TreeRef ref) {
  auto tree_node = lt.node(ref);
  const auto &n = lt.ir.node(tree_node.node);

  auto alloc = aux.allocs.at(lt.node(ref).node);

  if (n.op() == "add") {
    return gen_add(lt, aux.allocs, ref);
  } else if (n.op() == "mul") {
    return gen_mul(lt, aux.allocs, ref);
  } else if (n.op() == "read") {
    return gen_read(lt, ref, alloc);
  } else if (n.op() == "write") {
    return gen_write(lt, aux.allocs, ref);
  }
  return [=](const std::vector<void *> &memory, int indices[MAX_DEPTH],
             int tails[MAX_DEPTH]) {
    ASSERT(0);
    return;
  };
}

std::function<void(const std::vector<void *> &)>
gen_mem(const LoopTree &lt, const Auxiliary &aux, LoopTree::TreeRef ref) {
  // does this loop need to reset anything?
  std::vector<Allocation> reset_allocs =
      aux.resets.count(ref) ? aux.resets.at(ref) : std::vector<Allocation>{};
  auto alloc_off = lt.ir.inputs().size() + lt.ir.outputs().size();

  return [=](const std::vector<void *> &memory) {
    for (auto alloc : reset_allocs) {
      auto idx = alloc.idx + alloc_off;
      // std::cerr << "reseting " <<idx << "\n";
      if (alloc.init_val == 0) {
        memset(memory[idx], 0, sizeof(float) * alloc.size);
      } else {
        for (auto i = 0; i < alloc.size; ++i) {
          ((float *)memory[idx])[i] = alloc.init_val;
        }
      }
    }
  };
}

InnerFnType gen_loop(const LoopTree &lt, const Auxiliary &aux,
                     LoopTree::TreeRef ref) {
  auto tree_node = lt.node(ref);
  auto depth = tree_node.depth;
  auto loop = tree_node.loop;
  auto size = loop.size;
  auto tail_size = loop.tail;
  auto var_idx = aux.var_idx.at(loop.var);

  ASSERT(size > 0);
  ASSERT(tail_size >= 0);
  std::vector<InnerFnType> fns;
  for (auto c : tree_node.children) {
    fns.emplace_back(gen_fn(lt, aux, c));
  }

  auto inner_size = aux.inner_size.at(ref);

  auto memory_fn = gen_mem(lt, aux, ref);

  return [=](const std::vector<void *> &memory, int indices[MAX_DEPTH],
             int tails[MAX_DEPTH]) {
    auto run = [&](int n_size, int t_size) {
      for (auto i = 0; i < n_size; ++i) {
        memory_fn(memory);
        for (const auto &fn : fns) {
          indices[depth] = i;
          tails[var_idx] = 0;
          fn(memory, indices, tails);
        }
      }
      if (t_size) {
        memory_fn(memory);
        for (const auto &fn : fns) {
          indices[depth] = n_size;
          tails[var_idx] = t_size;
          fn(memory, indices, tails);
        }
      }
    };

    auto tail = tails[var_idx];
    if (tail) {
      auto N = tail / inner_size;
      auto T = tail % inner_size;
      run(N, T);
      return;
    }

    run(size, tail_size);
  };
}

void update_inner_size(
    const LoopTree &lt,
    std::unordered_map<LoopTree::TreeRef, size_t> &inner_size,
    LoopTree::TreeRef ref) {
  // can only be done with leaf nodes
  ASSERT(lt.node(ref).kind == LoopTree::NODE);
  auto loop_ref = lt.parent(ref);
  std::unordered_map<IR::VarRef, std::pair<int, int>> var_sizes;
  while (loop_ref != -1) {
    auto loop = lt.node(loop_ref).loop;
    if (!var_sizes.count(loop.var)) {
      var_sizes[loop.var] = std::make_pair(1, 0);
    }
    auto s = var_sizes[loop.var];
    auto old_size = s.first + s.second;
    if (inner_size.count(loop_ref)) {
      ASSERT(inner_size[loop_ref] == old_size);
    } else {
      inner_size[loop_ref] = old_size;
    }
    auto new_size = loop.size * old_size;
    var_sizes[loop.var] = std::make_pair(new_size, loop.tail);
    loop_ref = lt.parent(loop_ref);
  }
}

InnerFnType gen_fn(const LoopTree &lt, const Auxiliary &aux,
                   LoopTree::TreeRef ref) {
  for (const auto &codegen : getBackends()) {
    auto opt = codegen(lt, aux, ref);
    if (opt) {
      return opt;
    }
  }

  ASSERT(lt.node(ref).depth < MAX_DEPTH);
  if (lt.node(ref).kind == LoopTree::NODE) {
    return gen_leaf(lt, aux, ref);
  } else {
    return gen_loop(lt, aux, ref);
  }
}

// recursively calculate all auxilary information
void gen_aux(const LoopTree &lt, Auxiliary &aux, LoopTree::TreeRef ref) {
  ASSERT(lt.node(ref).depth < MAX_DEPTH);
  for (const auto &calc : getBackendsAux()) {
    if (calc(lt, aux, ref)) {
      return;
    }
  }
  if (lt.node(ref).kind == LoopTree::NODE) {
    update_inner_size(lt, aux.inner_size, ref);
    gen_alloc(lt, aux, ref);
  } else {
    auto loop = lt.node(ref).loop;
    if (!aux.var_idx.count(loop.var)) {
      auto idx = aux.var_idx.size();
      aux.var_idx[loop.var] = idx;
    }
    for (auto c : lt.node(ref).children) {
      gen_aux(lt, aux, c);
    }
  }
}

Auxiliary calculate_aux(const LoopTree &lt) {
  Auxiliary aux;
  for (auto root : lt.roots) {
    gen_aux(lt, aux, root);
  }
  return aux;
}

// function + sizes for intermediates
std::pair<std::function<void(const std::vector<void *> &)>, std::vector<size_t>>
compile(const LoopTree &lt) {
  Auxiliary aux = calculate_aux(lt);

  std::vector<InnerFnType> fns;
  for (auto root : lt.roots) {
    fns.emplace_back(gen_fn(lt, aux, root));
  }
  auto memory_fn = gen_mem(lt, aux, -1);

  auto fn = [=](const std::vector<void *> &memory) {
    memory_fn(memory);
    for (const auto &fn : fns) {
      int indices[MAX_DEPTH] = {0};
      int tails[MAX_DEPTH] = {0};
      fn(memory, indices, tails);
    }
  };

  std::vector<size_t> sizes;
  sizes.resize(aux.allocs.size());
  for (const auto &p : aux.allocs) {
    auto sizes_idx = p.second.idx;
    ASSERT(sizes.size() > sizes_idx);
    ASSERT(sizes_idx > -1);
    sizes[sizes_idx] = p.second.size * sizeof(float);
  }
  return std::make_pair(fn, sizes);
};

void exec(const LoopTree &lt, const std::vector<void *> &memory) {
  auto p = compile(lt);
  auto c = p.first;
  if (0) {
    auto start = std::chrono::steady_clock::now();
    auto iters = 1000;
    for (auto i = 0; i < iters; ++i) {
      p = compile(lt);
    }
    auto end = std::chrono::steady_clock::now();
    std::chrono::duration<double> diff = end - start;
    std::cerr << iters / diff.count() << " iters/sec\n";
  }
  auto memory_w_intermediates = memory;
  std::vector<void *> free_me;
  for (auto s : p.second) {
    memory_w_intermediates.emplace_back(calloc(1, s));
    free_me.emplace_back(memory_w_intermediates.back());
  }

  c(memory_w_intermediates);
  if (0) {
    auto start = std::chrono::steady_clock::now();
    auto iters = 10000;
    for (auto i = 0; i < iters; ++i) {
      c(memory_w_intermediates);
    }
    auto end = std::chrono::steady_clock::now();
    std::chrono::duration<double> diff = end - start;
    std::cerr << iters / diff.count() << " iters/sec\n";
  }
  for (auto v : free_me) {
    free(v);
  }
}
