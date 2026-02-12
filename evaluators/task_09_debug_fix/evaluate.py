#!/usr/bin/env python3
"""Evaluator for Task 09: Debug & Fix"""
import sys
import os
import importlib.util
import threading
import queue

TASK_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        '..', '..', 'tasks', 'task_09_debug_fix')
TIMEOUT = 2  # seconds per individual test call


def _call_with_timeout(fn, timeout):
    """Run fn() in a daemon thread.

    Returns:
        ('ok', value)      — fn() returned normally
        ('err', exception) — fn() raised an exception
        ('timeout', None)  — fn() did not finish within timeout seconds
    """
    result_q = queue.Queue()

    def worker():
        try:
            result_q.put(('ok', fn()))
        except Exception as e:
            result_q.put(('err', e))

    t = threading.Thread(target=worker, daemon=True)
    t.start()
    t.join(timeout)
    if t.is_alive():
        return 'timeout', None
    try:
        return result_q.get_nowait()
    except queue.Empty:
        return 'timeout', None


def load_solution():
    path = os.path.join(TASK_DIR, 'buggy_code.py')
    if not os.path.exists(path):
        print("[FAIL] buggy_code.py not found")
        sys.exit(1)
    spec = importlib.util.spec_from_file_location("buggy_code", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_fresh():
    """Load a fresh copy of the module to avoid mutable-default contamination."""
    path = os.path.join(TASK_DIR, 'buggy_code.py')
    spec = importlib.util.spec_from_file_location("buggy_fresh", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


passed = failed = 0


def check(name, fn, expected):
    global passed, failed
    kind, val = _call_with_timeout(fn, TIMEOUT)
    if kind == 'timeout':
        print(f"[FAIL] {name}: timed out after {TIMEOUT}s (infinite loop - bug not fixed)")
        failed += 1
    elif kind == 'err':
        print(f"[FAIL] {name}: {type(val).__name__}: {val}")
        failed += 1
    elif val == expected:
        print(f"[PASS] {name}")
        passed += 1
    else:
        print(f"[FAIL] {name}: expected {expected!r}, got {val!r}")
        failed += 1


def main():
    sol = load_solution()

    # -- binary_search ---------------------------------------------------------
    # Bug: left = mid  should be  left = mid + 1
    arr = [1, 3, 5, 7, 9, 11, 13, 15]

    check("binary_search finds first element",   lambda: sol.binary_search(arr, 1),   0)
    check("binary_search finds last element",    lambda: sol.binary_search(arr, 15),  7)
    check("binary_search finds middle element",  lambda: sol.binary_search(arr, 7),   3)
    check("binary_search right-half element",    lambda: sol.binary_search(arr, 9),   4)
    check("binary_search returns -1 if missing", lambda: sol.binary_search(arr, 6),  -1)
    check("binary_search single element hit",    lambda: sol.binary_search([42], 42), 0)
    check("binary_search single element miss",   lambda: sol.binary_search([42], 0), -1)

    # -- make_list -------------------------------------------------------------
    # Bug: mutable default argument  def make_list(item, result=[])
    # Two calls on the SAME module instance expose the bug.
    def test_make_list_single():
        m = load_fresh()
        return m.make_list('x')

    def test_make_list_independence():
        m = load_fresh()
        m.make_list('first')           # seeds the bug if not fixed
        return m.make_list('second')   # bug returns ['first','second']; fixed returns ['second']

    check("make_list first call returns ['x']",      test_make_list_single,       ['x'])
    check("make_list second call is independent",    test_make_list_independence, ['second'])

    # -- is_palindrome ---------------------------------------------------------
    # Bug: cleaned[1:]  should be  cleaned[::-1]
    check("is_palindrome racecar",                   lambda: sol.is_palindrome("racecar"),                        True)
    check("is_palindrome multi-word palindrome",     lambda: sol.is_palindrome("A man a plan a canal Panama"),    True)
    check("is_palindrome hello is not palindrome",   lambda: sol.is_palindrome("hello"),                          False)
    check("is_palindrome single char",               lambda: sol.is_palindrome("a"),                              True)
    check("is_palindrome empty string",              lambda: sol.is_palindrome(""),                               True)

    # -- max_sliding_window ----------------------------------------------------
    # Bug: range(len(arr) - k)  should be  range(len(arr) - k + 1)
    check("sliding window standard case",
          lambda: sol.max_sliding_window([1, 3, -1, -3, 5, 3, 6, 7], 3), [3, 3, 5, 5, 6, 7])
    check("sliding window k=1",
          lambda: sol.max_sliding_window([4, 2, 7], 1),                   [4, 2, 7])
    check("sliding window k=len(arr)",
          lambda: sol.max_sliding_window([1, 5, 2], 3),                   [5])
    check("sliding window all same values",
          lambda: sol.max_sliding_window([3, 3, 3, 3], 2),                [3, 3, 3])

    print(f"\nResults: {passed}/{passed + failed} tests passed")
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
