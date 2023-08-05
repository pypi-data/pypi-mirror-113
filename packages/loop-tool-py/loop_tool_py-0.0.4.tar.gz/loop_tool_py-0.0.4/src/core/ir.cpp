/*
Copyright (c) Facebook, Inc. and its affiliates.

This source code is licensed under the MIT license found in the
LICENSE file in the root directory of this source tree.
*/
#include "ir.h"
#include <algorithm>
#include <iostream>
#include <sstream>
#include <tuple>
#include <unordered_map>
#include <unordered_set>

IR::VarRef IR::create_var(std::string name) {
  auto version = 0;
  for (const auto &v : vars_) {
    if (v.name() == name) {
      version++;
    }
  }
  Var v(name, version);
  int new_idx = vars_.size();
  vars_.emplace_back(v);
  return new_idx;
}

IR::NodeRef IR::create_node(std::string op, std::vector<IR::NodeRef> inputs,
                            std::vector<IR::VarRef> vars) {
  IR::NodeRef new_idx = nodes_.size();
  Node n_(op, inputs, vars);

  // auxiliary information
  nodes_.emplace_back(std::move(n_));
  priorities_.emplace_back(0);
  orders_.emplace_back();
  reuse_disabled_.emplace_back();
  reset_aux(new_idx);

  for (const auto &idx : inputs) {
    node(idx).outputs_.emplace_back(new_idx);
  }
  return new_idx;
}

void IR::reset_aux(IR::NodeRef node_ref) {
  // TODO attempt to preserve old order
  std::vector<std::pair<IR::NodeRef, IR::LoopSize>> order;
  for (const auto &v : all_vars(node_ref)) {
    order.emplace_back(v, IR::LoopSize{-1, -1});
  }
  priorities_[node_ref] = 0;
  reuse_disabled_[node_ref].clear();
  orders_[node_ref] = order;
}

void IR::replace_all_uses(NodeRef old_node, NodeRef new_node) {
  auto &outputs = node(old_node).outputs();
  for (auto out : outputs) {
    node(out).replace_input(old_node, new_node);
  }
  node(new_node).update_outputs(outputs);
  node(old_node).update_outputs({});
}

void IR::update_inputs(NodeRef node_ref, std::vector<NodeRef> inputs) {
  ASSERT(node(node_ref).inputs().size() == 0 &&
         "TODO remove old inputs if they exist");
  node(node_ref).update_inputs(inputs);
  for (auto input : inputs) {
    auto &in_node = node(input);
    auto outputs = in_node.outputs();
    outputs.emplace_back(node_ref);
    in_node.update_outputs(outputs);
  }
}

void IR::update_vars(NodeRef node_ref, std::vector<VarRef> vars) {
  node(node_ref).update_vars(vars);
}

std::string IR::dump(IR::NodeRef idx) const {
  const auto &n = node(idx);
  std::stringstream ss;
  ss << "%" << idx << "[";
  for (const auto &v_idx : n.vars()) {
    const auto &v = var(v_idx);
    ss << v.name(); // << ":" << v.version();
    if (&v_idx != &n.vars().back()) {
      ss << ", ";
    }
  }
  ss << "] <- " << n.op() << "(";
  for (const auto &inp : n.inputs()) {
    ss << "%" << inp;
    if (&inp != &n.inputs().back()) {
      ss << ", ";
    }
  }
  ss << ")";
  return ss.str();
}

std::vector<IR::VarRef> IR::pointwise_vars(IR::NodeRef idx) const {
  auto var_vec = node(idx).vars();
  std::unordered_set<IR::VarRef> vars = {var_vec.begin(), var_vec.end()};
  std::vector<IR::VarRef> pointwise_vars;
  for (auto inp : inputs()) {
    for (auto v : node(inp).vars()) {
      if (vars.count(v)) {
        vars.erase(v);
      }
    }
  }
  for (auto v : var_vec) {
    if (vars.count(v)) {
      continue;
    }
    pointwise_vars.emplace_back(v);
  }
  return pointwise_vars;
}

std::vector<IR::VarRef> IR::all_vars(IR::NodeRef idx) const {
  auto var_vec = node(idx).vars();
  std::unordered_set<IR::VarRef> vars = {var_vec.begin(), var_vec.end()};
  std::vector<IR::VarRef> all_vars = var_vec;
  for (auto inp : node(idx).inputs()) {
    for (auto v : node(inp).vars()) {
      if (vars.count(v)) {
        continue;
      }
      all_vars.emplace_back(v);
      vars.insert(v);
    }
  }
  std::sort(all_vars.begin(), all_vars.end());
  return all_vars;
}

std::vector<IR::VarRef> IR::vars() const {
  std::vector<IR::VarRef> vs;
  for (auto i = 0; i < vars_.size(); ++i) {
    vs.emplace_back(i);
  }
  return vs;
}

std::vector<IR::NodeRef> IR::nodes() const {
  std::vector<IR::NodeRef> ns;
  for (auto i = 0; i < nodes_.size(); ++i) {
    ns.emplace_back(i);
  }
  return ns;
}

void Node::replace_input(IR::NodeRef old_node, IR::NodeRef new_node) {
  for (auto &n : inputs_) {
    if (n == old_node) {
      n = new_node;
    }
  }
}

IR split_node(const IR &ir, IR::NodeRef node_ref,
              std::vector<IR::VarRef> injected) {
  IR new_ir = ir;
  auto &node = new_ir.node(node_ref);
  auto vs_vec = new_ir.all_vars(node_ref);
  std::unordered_set<IR::VarRef> vs{vs_vec.begin(), vs_vec.end()};
  for (auto v : injected) {
    ASSERT(vs.count(v));
    vs.erase(v);
  }
  ASSERT(vs.size() > 0);
  auto new_node_ref = new_ir.create_node(node.op(), {}, node.vars());
  new_ir.replace_all_uses(node_ref, new_node_ref);
  new_ir.update_vars(node_ref, injected);
  new_ir.update_inputs(new_node_ref, {node_ref});
  new_ir.reset_aux(node_ref);
  new_ir.reset_aux(new_node_ref);
  return new_ir;
}

// new IR is generated
IR split_var(const IR &ir_, IR::VarRef v) {
  ASSERT(0 && "not yet implemented");
  auto ir = ir_;
  return ir;
}

std::vector<IR::NodeRef> toposort(const IR &ir) {
  std::vector<IR::NodeRef> sorted;
  // prioritized node indices
  std::vector<std::pair<IR::NodeRef, float>> frontier;
  for (const auto &idx : ir.inputs()) {
    frontier.emplace_back(std::make_pair(idx, ir.priority(idx)));
  }

  std::unordered_set<IR::NodeRef> seen; // to keep track of in-edges
  while (frontier.size()) {
    std::stable_sort(
        frontier.begin(), frontier.end(),
        [](std::pair<IR::NodeRef, float> a, std::pair<IR::NodeRef, float> b) {
          return a.second > b.second;
        });
    auto cur_idx = frontier.front().first;
    sorted.emplace_back(cur_idx);
    seen.insert(cur_idx);
    frontier.erase(frontier.begin());
    // check if we've visited all the inputs to any dependent nodes
    for (const auto &dep : ir.node(cur_idx).outputs()) {
      const auto &in = ir.node(dep).inputs();
      bool traversed = std::all_of(
          in.begin(), in.end(), [&](IR::NodeRef i) { return seen.count(i); });
      if (traversed) {
        frontier.emplace_back(std::make_pair(dep, ir.priority(dep)));
      }
    }
  }
  return sorted;
}

LoopTree::TreeRef LoopTree::add_leaf(LoopTree::TreeRef parent, IR::NodeRef n) {
  return add_node_impl(parent, n);
}

LoopTree::TreeRef LoopTree::add_loop(LoopTree::TreeRef parent,
                                     const LoopTree::Loop &l) {
  return add_node_impl(parent, l);
}

void LoopTree::walk(const std::function<void(LoopTree::TreeRef, int)> &fn,
                    LoopTree::TreeRef start) const {
  std::function<void(LoopTree::TreeRef tr, int d)> inner_walk;
  inner_walk = [&](LoopTree::TreeRef tr, int d) {
    fn(tr, d);
    for (auto c : node(tr).children) {
      inner_walk(c, d + 1);
    }
  };
  if (start == -1) {
    for (auto root : roots) {
      inner_walk(root, 0);
    }
  } else {
    inner_walk(start, 0);
  }
}

LoopTree::TreeRef LoopTree::lca(LoopTree::TreeRef a,
                                LoopTree::TreeRef b) const {
  auto traverse = [&](LoopTree::TreeRef n, int d) {
    for (auto i = 0; i < d; ++i) {
      n = node(n).parent;
    }
    return n;
  };
  if (a == -1 || b == -1) {
    return -1;
  }
  if (node(a).depth > node(b).depth) {
    a = traverse(a, node(a).depth - node(b).depth);
  } else if (node(b).depth > node(a).depth) {
    b = traverse(b, node(b).depth - node(a).depth);
  }
  ASSERT(node(a).depth == node(b).depth);
  while (a != b) {
    a = traverse(a, 1);
    b = traverse(b, 1);
  }
  ASSERT(a == b);
  return a;
}

std::string
LoopTree::dump(const std::function<std::string(LoopTree::TreeRef)> &fn) const {
  std::stringstream ss;
  walk([&](LoopTree::TreeRef tr, int d) {
    for (auto i = 0; i < d; ++i) {
      ss << " ";
    }
    auto tn = node(tr);
    if (tn.kind == 0) {
      ss << ir.dump(tn.node);
      if (fn) {
        ss << " " << fn(tr);
      }
      ss << "\n";
    } else {
      ss << "for " << ir.var(tn.loop.var).name();
      for (auto i = 0; i < tn.loop.var_depth; ++i) {
        ss << "'";
      }
      auto s = tn.loop.size;
      auto t = tn.loop.tail;
      if (s > -1) {
        ss << " in " << s;
      }
      if (t > 0) {
        ss << " r " << t;
      }
      ss << " : L" << tr;
      if (fn) {
        ss << " " << fn(tr);
      }
      ss << "\n";
    }
  });
  return ss.str();
}
std::vector<LoopTree::Loop> LoopTree::loop_order(IR::NodeRef ref) const {
  auto order = ir.order(ref);
  std::vector<LoopTree::Loop> out;
  std::unordered_map<IR::VarRef, int> count;
  for (const auto &p : order) {
    LoopTree::Loop l = {p.first, count[p.first], p.second.size, p.second.tail};
    count[p.first]++;
    out.emplace_back(l);
  }
  return out;
}

LoopTree::LoopTree(const IR &ir_) : ir(ir_) {
  LoopTree::TreeRef ln = -1;

  std::vector<std::pair<LoopTree::Loop, LoopTree::TreeRef>> available;
  using Iterator = typename decltype(available)::iterator;

  std::vector<IR::NodeRef> order = toposort(ir);
  for (const auto &idx : order) {
    auto n = ir.node(idx);
    auto l_order = loop_order(idx);
    // find max reuse O(n^2)
    // 1. find all reuse candidates and enumerate them with respect to
    // the proposed order:
    //   e.g. (0, loop0), (1, loop2), (2, loop3) ...
    //   e.g. (0, loop2), (1, loop1), (2, loop3) ...
    //   e.g. (0, loop1), (1, loop3), (2, loop2) ...
    // 2. sort by loop (second elem)
    //   e.g. (0, loop0), (1, loop2), (2, loop3) ...
    //   e.g. (1, loop1), (0, loop2), (2, loop3) ...
    //   e.g. (0, loop1), (2, loop2), (1, loop3) ...
    // it's clear that we can reuse everyting in the first example
    // and nothing in the second example. For the third,
    // simply track the first arg in order: we can reuse loop1 and that's it

    // prune mismatched loop sizes
    for (auto i = 0; i < l_order.size(); ++i) {
      const auto &loop = l_order[i];
      auto iter =
          std::find_if(available.begin(), available.end(),
                       [&](std::pair<LoopTree::Loop, LoopTree::TreeRef> &t) {
                         // same var, different splits
                         // TODO audit versioning
                         return (loop.var == t.first.var) &&
                                (loop.var_depth == t.first.var_depth) &&
                                !(t.first == loop);
                       });
      available.erase(iter, available.end());
    }
    // std::cout << "avail after removing mismatch sizes " << available.size()
    // << "\n";
    // find matched loops
    std::vector<std::pair<int, int>> reuse_candidates;
    for (auto i = 0; i < l_order.size(); ++i) {
      const auto &loop = l_order[i];
      auto iter =
          std::find_if(available.begin(), available.end(),
                       [&](std::pair<LoopTree::Loop, LoopTree::TreeRef> &t) {
                         return t.first == loop;
                       });
      int offset = iter - available.begin();
      reuse_candidates.emplace_back(i, offset);
    }
    // std::cout << "number of reuse candidates: " << reuse_candidates.size() <<
    // "\n";
    std::stable_sort(
        reuse_candidates.begin(), reuse_candidates.end(),
        [](const std::pair<int, int> &a, const std::pair<int, int> &b) {
          return a.second < b.second;
        });
    auto reuse = available.begin();
    auto first = l_order.begin();
    for (auto i = 0; i < l_order.size(); ++i) {
      auto offset = reuse_candidates[i].second;
      if (i != reuse_candidates[i].first || offset == available.size()) {
        // std::cout << "breaking after " << i << " because " << (i !=
        // reuse_candidates[i].first) << " or " <<  (offset == available.size())
        // << "\n"; std::cout << "offset is " << offset << " but available size
        // is " << available.size() << "\n";
        break;
      }
      reuse = available.begin() + (offset + 1);
      first++;
    }
    // std::cout << "first: " << std::distance(first, l_order.begin()) << "\n";

    for (; first != l_order.end(); first++) {
      LoopTree::Loop loop = *first;
      auto parent = reuse != available.begin() ? (reuse - 1)->second : -1;
      LoopTree::TreeRef loc = add_loop(parent, loop);
      available.erase(reuse, available.end());
      available.emplace_back(loop, loc);
      reuse = available.end();
    }
    LoopTree::TreeRef parent = -1;
    if (available.size()) {
      parent = available.back().second;
    }
    add_leaf(parent, idx);

    // std::cout << "avail after adding stuff " << available.size() << "\n";
    // remove reductions
    std::unordered_set<IR::VarRef> reduction_vars;
    for (const auto &inp : n.inputs()) {
      const auto &v = ir.node(inp).vars();
      reduction_vars.insert(v.begin(), v.end());
    }
    for (const auto &v : n.vars()) {
      if (reduction_vars.count(v)) {
        reduction_vars.erase(v);
      }
    }
    auto iter =
        std::find_if(available.begin(), available.end(),
                     [&](std::pair<LoopTree::Loop, LoopTree::TreeRef> &t) {
                       return reduction_vars.count(t.first.var);
                     });
    available.erase(iter, available.end());
    // std::cout << "avail after reduction elim " << available.size() << "\n";

    for (auto no_reuse : ir.not_reusable(idx)) {
      auto iter =
          std::find_if(available.begin(), available.end(),
                       [&](std::pair<LoopTree::Loop, LoopTree::TreeRef> &t) {
                         return t.first == l_order[no_reuse];
                       });
      available.erase(iter, available.end());
    }
    // std::cout << "avail after no_reuse " << available.size() << "\n";
  }
}

std::string dot(const IR &ir) {
  std::stringstream ss;
  ss << "digraph G {\n";
  for (auto n : toposort(ir)) {
    ss << " ";
    ss << n << "[label=\"" << ir.dump(n) << "\"];\n";
    for (auto out : ir.node(n).outputs()) {
      ss << " " << n << " -> " << out << ";\n";
    }
  }
  ss << "}\n";
  return ss.str();
}
