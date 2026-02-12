# Task 03: Binary Search Tree (Python)

Implement a Binary Search Tree (BST) in `bst.py`.

## Background

A Binary Search Tree is a tree data structure where each node holds a key and:
- All keys in the **left** subtree are **less than** the node's key.
- All keys in the **right** subtree are **greater than** the node's key.

This property enables efficient search, insert, and delete in O(log n) average time.

## What to implement

### `class BSTNode`
A tree node holding `key`, `left`, and `right` attributes.

### `class BinarySearchTree`

#### `insert(key)` → `None`
Insert `key` into the BST.  Duplicate keys should be ignored.

#### `search(key)` → `bool`
Return `True` if `key` exists in the tree, `False` otherwise.

#### `delete(key)` → `None`
Remove `key` from the BST.  Handle all three cases:
1. Node is a leaf → remove it directly.
2. Node has one child → replace it with that child.
3. Node has two children → replace with its **in-order successor** (smallest key in the right subtree), then delete the successor from the right subtree.

If `key` is not present, do nothing.

#### `inorder()` → `list`
Return a list of all keys in ascending (in-order) order.

#### `height()` → `int`
Return the height of the tree (number of edges on the longest root-to-leaf path).
An empty tree has height `-1`; a single-node tree has height `0`.

#### `min_value()` → value or `None`
Return the minimum key in the tree, or `None` if the tree is empty.

## File to modify

**`bst.py`** — implement `BSTNode` and `BinarySearchTree`.
