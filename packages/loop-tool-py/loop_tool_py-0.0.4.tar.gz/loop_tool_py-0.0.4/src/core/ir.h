/*
Copyright (c) Facebook, Inc. and its affiliates.

This source code is licensed under the MIT license found in the
LICENSE file in the root directory of this source tree.
*/
#pragma once

#include "error.h"
#include <cassert>
#include <functional>
#include <string>
#include <unordered_set>
#include <vector>

/*
  Intermediate represention is a DAG

  Two nodes: value, compute -- their placement in the loop tree matters
  For value nodes there are three annotations:
    read, write, view -- they all contain index information

  This DAG is then realized into a Tree

  Branches annotated by (variable, size) pair
  Leafs contain either value or compute nodes

  Invariants:
    - var \in ancestors \all var \in vars(leaf)
    - \all{var, leaf} \prod {size(loop) \in ancestor(leaf) | var \in loop}  ==
  size(var)

  transpose:

  for a in 128 by 30:
    for b in 11:
      for a' in 30 by 7:
        for a" in 7:
          B[b, a] = A[a, b]


  Transforms:
  (all splits implicitly mergeable)
   DFG transforms:
    split var
    swap var
    split (clone?) value
   Loop tree transforms (annotations on DFG):
    split loop for leaf (tiling etc)
    set loop order of leaf (reordering)
    set loop exclusivity of leaf (force writes to memory)
    set execution priority of leaf (toposort priority)

  DFG -> tree algo
  1. prioritized toposort
  2. emit loop order of first leaf, saving availability
    availability = all (var,size) pairs - (reduction vars + exclusive loops)
  3. get next leaf
    a. get loop in order
    b. if loop is available and no later loops are available before it, reuse it
    c. else update availability
    d. go to a
    this maximally reuses loops

  Example 1:

  for A
    for B
      for C
        for D
      for E

  available = A, B, E
  leaf order = A, B, C

  for A
    for B
      for C
        for D
      for E
      for C
        leaf

  Example 2:

  for A
    for B
      for C
        for D
      for E

  available = A, B, E
  leaf order = A, C, B

  for A
    for B
      for C
        for D
      for E
    for C
      for B
        leaf

*/

struct Node;
struct Var;

class IR {
public:
  IR() {}
  // For code clarity
  using NodeRef = int;
  using VarRef = int;
  struct LoopSize {
    int size;
    int tail;
  };

  NodeRef create_node(std::string op, std::vector<NodeRef> inputs,
                      std::vector<VarRef> vars);
  VarRef create_var(std::string name);

  void replace_all_uses(NodeRef old_node, NodeRef new_node);
  void update_inputs(NodeRef node_ref, std::vector<NodeRef> inputs);
  // void update_outputs(NodeRef node_ref, std::vector<NodeRef> outputs);
  void update_vars(NodeRef node_ref, std::vector<VarRef> vars);

  std::vector<VarRef> vars() const;
  std::vector<NodeRef> nodes() const;

  inline const Node &node(NodeRef idx) const {
    ASSERT(idx < nodes_.size());
    return nodes_[idx];
  }
  inline Node &node(NodeRef idx) {
    ASSERT(idx < nodes_.size());
    return nodes_[idx];
  }

  inline const Var &var(VarRef idx) const {
    ASSERT(idx < vars_.size());
    return vars_[idx];
  }
  inline Var &var(VarRef idx) {
    ASSERT(idx < vars_.size());
    return vars_[idx];
  }

  inline float priority(NodeRef idx) const { return priorities_[idx]; }
  // order (int,int)[] - first = var, second = size (possibly -1)
  inline const std::vector<std::pair<VarRef, LoopSize>> &
  order(NodeRef idx) const {
    return orders_[idx];
  }
  inline const std::unordered_set<int> not_reusable(NodeRef idx) const {
    return reuse_disabled_[idx];
  }

  inline const std::vector<NodeRef> &inputs() const { return inputs_; }
  inline const std::vector<NodeRef> &outputs() const { return outputs_; }

  inline void set_inputs(std::vector<NodeRef> inputs) {
    inputs_ = std::move(inputs);
  }
  inline void set_outputs(std::vector<NodeRef> outputs) {
    outputs_ = std::move(outputs);
  }

  // auxiliary information / annotations
  void reset_aux(IR::NodeRef node_ref);
  inline void set_priority(NodeRef idx, float priority) {
    priorities_[idx] = priority;
  }
  inline void set_order(NodeRef idx,
                        std::vector<std::pair<VarRef, LoopSize>> order) {
    // TODO validate order
    orders_[idx] = order;
  }
  inline void disable_reuse(NodeRef idx, int order_idx) {
    reuse_disabled_[idx].insert(order_idx);
  }
  inline void enable_reuse(NodeRef idx, int order_idx) {
    reuse_disabled_[idx].erase(order_idx);
  }

  std::string dump(NodeRef idx) const;
  std::vector<VarRef> pointwise_vars(NodeRef idx) const;
  std::vector<VarRef> all_vars(NodeRef idx) const;

private:
  std::vector<Node> nodes_;
  // TODO consider efficient storage for splits/merges
  std::vector<Var> vars_;
  std::vector<float> priorities_;
  std::vector<std::vector<std::pair<VarRef, LoopSize>>> orders_;
  std::vector<std::unordered_set<int>> reuse_disabled_;
  std::vector<NodeRef> inputs_;
  std::vector<NodeRef> outputs_;
};

// new IR is generated
IR split_node(const IR &ir, IR::NodeRef node_ref,
              std::vector<IR::VarRef> injected);
IR split_var(const IR &ir, IR::VarRef v);
std::string dot(const IR &ir);

class Node {
protected:
  friend class IR; // use the IR class to create nodes
  Node(std::string op, std::vector<IR::NodeRef> inputs,
       std::vector<IR::VarRef> vars)
      : op_(op), inputs_(inputs), vars_(vars) {}

  void replace_input(IR::NodeRef old_node, IR::NodeRef new_node);
  inline void update_inputs(std::vector<IR::NodeRef> inputs) {
    inputs_ = inputs;
  }
  inline void update_outputs(std::vector<IR::NodeRef> outputs) {
    outputs_ = outputs;
  }
  inline void update_vars(std::vector<IR::VarRef> vars) { vars_ = vars; }

public:
  inline const std::vector<IR::NodeRef> &inputs() const { return inputs_; }
  inline const std::vector<IR::NodeRef> &outputs() const { return outputs_; }

  const std::string &op() const { return op_; }
  const std::vector<IR::VarRef> &vars() const { return vars_; }

private:
  std::string op_;
  std::vector<IR::NodeRef> inputs_;
  // denote the output vars
  std::vector<IR::VarRef> vars_;

protected:
  std::vector<IR::NodeRef> outputs_;
};

class Var {
public:
  Var(std::string name, int version) : name_(name), version_(version) {}
  inline const std::string &name() const { return name_; }
  inline const int &version() const { return version_; }

private:
  std::string name_;
  int version_;
};

// cheap, disposable data structures
struct LoopTree {
  using TreeRef = int;
  enum { NODE = 0, LOOP = 1 };

  struct Loop {
    IR::VarRef var;
    int var_depth;
    int size;
    int tail;
    bool operator==(const Loop &other) const {
      return var == other.var && var_depth == other.var_depth &&
             size == other.size && tail == other.tail;
    }
  };

  struct LoopNode {
    TreeRef parent = -1;
    TreeRef idx = -1;
    int depth = 0; // root depth

    bool kind; // 0 -> node, 1 -> loop
    union {
      IR::NodeRef node;
      Loop loop;
    };

    std::vector<int> children;

    LoopNode(int p, int i, IR::NodeRef n)
        : parent(p), idx(i), node(n), kind(0) {}
    LoopNode(int p, int i, const Loop &l)
        : parent(p), idx(i), loop(l), kind(1) {}
  };

  TreeRef add_leaf(TreeRef parent, IR::NodeRef n);
  TreeRef add_loop(TreeRef parent, const Loop &l);
  template <typename T> TreeRef add_node_impl(TreeRef parent, T n) {
    auto new_idx = nodes.size();
    nodes.emplace_back(parent, new_idx, n);
    if (parent == -1) {
      roots.emplace_back(new_idx);
      nodes[new_idx].depth = 0;
    } else {
      auto &parent_node = nodes[parent];
      nodes[new_idx].depth = parent_node.depth + 1;
      parent_node.children.emplace_back(new_idx);
    }
    return new_idx;
  }

  // TODO rename this
  inline const LoopNode &node(TreeRef idx) const {
    ASSERT(idx < nodes.size());
    return nodes[idx];
  }
  inline const TreeRef parent(TreeRef idx) const {
    ASSERT(idx < nodes.size());
    return nodes[idx].parent;
  }
  TreeRef lca(TreeRef a, TreeRef b) const;

  // like IR::order but includes variable versions
  std::vector<LoopTree::Loop> loop_order(IR::NodeRef ref) const;

  std::vector<LoopNode> nodes;
  std::vector<TreeRef> roots;
  void walk(const std::function<void(LoopTree::TreeRef, int)> &fn,
            TreeRef start = -1) const;
  std::string
  dump(const std::function<std::string(LoopTree::TreeRef)> &fn = {}) const;
  IR ir;

  LoopTree(const IR &ir_);
};
