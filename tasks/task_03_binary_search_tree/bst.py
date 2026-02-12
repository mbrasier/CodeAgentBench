from typing import Optional, List


class BSTNode:
    """A node in a Binary Search Tree."""

    def __init__(self, key):
        self.key = key
        self.left: Optional['BSTNode'] = None
        self.right: Optional['BSTNode'] = None


class BinarySearchTree:
    """Binary Search Tree with insert, search, delete, and traversal."""

    def __init__(self):
        self.root: Optional[BSTNode] = None

    def insert(self, key) -> None:
        """Insert key into the BST. Duplicate keys are ignored."""
        raise NotImplementedError

    def search(self, key) -> bool:
        """Return True if key exists in the BST, False otherwise."""
        raise NotImplementedError

    def delete(self, key) -> None:
        """Remove key from the BST.

        Handles three cases:
          1. Leaf node: remove directly.
          2. One child: replace node with its child.
          3. Two children: replace with in-order successor, then delete successor.

        Does nothing if key is not in the tree.
        """
        raise NotImplementedError

    def inorder(self) -> List:
        """Return all keys in ascending order via in-order traversal."""
        raise NotImplementedError

    def height(self) -> int:
        """Return the height of the tree.

        Empty tree → -1.  Single node → 0.
        """
        raise NotImplementedError

    def min_value(self):
        """Return the minimum key, or None if the tree is empty."""
        raise NotImplementedError
