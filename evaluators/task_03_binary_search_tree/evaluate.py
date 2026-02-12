#!/usr/bin/env python3
"""Evaluator for Task 03: Binary Search Tree"""
import sys
import os
import importlib.util

TASK_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        '..', '..', 'tasks', 'task_03_binary_search_tree')


def load_solution():
    path = os.path.join(TASK_DIR, 'bst.py')
    if not os.path.exists(path):
        print("[FAIL] bst.py not found")
        sys.exit(1)
    spec = importlib.util.spec_from_file_location("bst", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


passed = failed = 0


def check(name, fn, expected):
    global passed, failed
    try:
        got = fn()
        if got == expected:
            print(f"[PASS] {name}")
            passed += 1
        else:
            print(f"[FAIL] {name}: expected {expected!r}, got {got!r}")
            failed += 1
    except NotImplementedError:
        print(f"[FAIL] {name}: not implemented")
        failed += 1
    except Exception as e:
        print(f"[FAIL] {name}: {type(e).__name__}: {e}")
        failed += 1


def main():
    sol = load_solution()
    BST = sol.BinarySearchTree

    # ── Search & insert ──────────────────────────────────────────────────────
    check("search empty tree", lambda: BST().search(5), False)

    def t_insert_search():
        b = BST()
        for k in [5, 3, 7, 1, 4]:
            b.insert(k)
        return b.search(4) and b.search(1) and not b.search(9)

    check("insert and search", t_insert_search, True)

    check("duplicate insert ignored", lambda: (
        lambda b: (b.insert(5), b.insert(5), b.inorder())
    )(BST())[2], [5])

    # ── Inorder traversal ───────────────────────────────────────────────────
    def t_inorder():
        b = BST()
        for k in [5, 3, 7, 1, 4, 6, 8]:
            b.insert(k)
        return b.inorder()

    check("inorder returns sorted list", t_inorder, [1, 3, 4, 5, 6, 7, 8])
    check("inorder empty tree", lambda: BST().inorder(), [])

    # ── Height ──────────────────────────────────────────────────────────────
    check("height empty tree", lambda: BST().height(), -1)

    check("height single node", lambda: (
        lambda b: (b.insert(5), b.height())
    )(BST())[1], 0)

    def t_height():
        b = BST()
        for k in [5, 3, 7, 1]:
            b.insert(k)
        return b.height()

    check("height balanced tree", t_height, 2)

    # ── Min value ───────────────────────────────────────────────────────────
    check("min_value empty", lambda: BST().min_value(), None)

    def t_min():
        b = BST()
        for k in [5, 3, 7, 1, 9]:
            b.insert(k)
        return b.min_value()

    check("min_value", t_min, 1)

    # ── Delete ──────────────────────────────────────────────────────────────
    def t_delete_leaf():
        b = BST()
        for k in [5, 3, 7]:
            b.insert(k)
        b.delete(3)
        return b.inorder()

    check("delete leaf", t_delete_leaf, [5, 7])

    def t_delete_one_child():
        b = BST()
        for k in [5, 3, 7, 2]:
            b.insert(k)
        b.delete(3)   # has left child 2
        return b.inorder()

    check("delete node with one child", t_delete_one_child, [2, 5, 7])

    def t_delete_two_children():
        b = BST()
        for k in [5, 3, 7, 1, 4, 6, 8]:
            b.insert(k)
        b.delete(5)   # root, two children
        return b.inorder()

    check("delete node with two children", t_delete_two_children, [1, 3, 4, 6, 7, 8])

    def t_delete_nonexistent():
        b = BST()
        b.insert(5)
        b.delete(99)  # should not raise
        return b.inorder()

    check("delete nonexistent does nothing", t_delete_nonexistent, [5])

    print(f"\nResults: {passed}/{passed + failed} tests passed")
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
