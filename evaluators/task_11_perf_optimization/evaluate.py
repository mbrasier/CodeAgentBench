#!/usr/bin/env python3
"""Evaluator for Task 11: Performance Optimization"""
import sys
import os
import importlib.util
import time
import threading

TASK_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        '..', '..', 'tasks', 'task_11_perf_optimization')


def load_solution():
    path = os.path.join(TASK_DIR, 'slow_functions.py')
    if not os.path.exists(path):
        print("[FAIL] slow_functions.py not found")
        sys.exit(1)
    spec = importlib.util.spec_from_file_location("slow_functions", path)
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
    except Exception as e:
        print(f"[FAIL] {name}: {type(e).__name__}: {e}")
        failed += 1


def check_perf(name, fn, limit_s):
    """Run fn() in a daemon thread; fail if over limit_s or if it hangs."""
    global passed, failed
    exc = [None]

    def target():
        try:
            fn()
        except Exception as e:
            exc[0] = e

    hard_limit = max(limit_s * 5, 5.0)
    t = threading.Thread(target=target, daemon=True)
    t0 = time.time()
    t.start()
    t.join(timeout=hard_limit)
    elapsed = time.time() - t0

    if t.is_alive():
        print(f"[FAIL] {name}: timed out (limit {limit_s}s)")
        failed += 1
    elif exc[0] is not None:
        print(f"[FAIL] {name}: {type(exc[0]).__name__}: {exc[0]}")
        failed += 1
    elif elapsed <= limit_s:
        print(f"[PASS] {name} ({elapsed*1000:.1f}ms)")
        passed += 1
    else:
        print(f"[FAIL] {name}: took {elapsed:.2f}s (limit {limit_s}s)")
        failed += 1


def main():
    sol = load_solution()

    # -- has_duplicates correctness --------------------------------------------
    check("has_duplicates empty list",         lambda: sol.has_duplicates([]),         False)
    check("has_duplicates single element",     lambda: sol.has_duplicates([1]),        False)
    check("has_duplicates no duplicates",      lambda: sol.has_duplicates([1, 2, 3]),  False)
    check("has_duplicates with duplicate",     lambda: sol.has_duplicates([1, 2, 1]),  True)
    check("has_duplicates all same",           lambda: sol.has_duplicates([5, 5, 5]),  True)

    # -- has_duplicates performance --------------------------------------------
    big_list = list(range(100_000))
    check_perf("has_duplicates 100k distinct elements (no dupe)", lambda: sol.has_duplicates(big_list), 0.5)

    # -- fibonacci correctness -------------------------------------------------
    check("fibonacci(0)",  lambda: sol.fibonacci(0),  0)
    check("fibonacci(1)",  lambda: sol.fibonacci(1),  1)
    check("fibonacci(2)",  lambda: sol.fibonacci(2),  1)
    check("fibonacci(6)",  lambda: sol.fibonacci(6),  8)
    check("fibonacci(10)", lambda: sol.fibonacci(10), 55)

    # -- fibonacci performance -------------------------------------------------
    check_perf("fibonacci(40) fast", lambda: sol.fibonacci(40), 1.0)

    # -- find_common_elements correctness -------------------------------------
    check("find_common_elements empty",
          lambda: sorted(sol.find_common_elements([], [])), [])
    check("find_common_elements no overlap",
          lambda: sorted(sol.find_common_elements([1, 2], [3, 4])), [])
    check("find_common_elements some overlap",
          lambda: sorted(sol.find_common_elements([1, 2, 3], [2, 3, 4])), [2, 3])
    check("find_common_elements no duplicates in result",
          lambda: sorted(sol.find_common_elements([1, 1, 2], [1, 2])), [1, 2])

    # -- find_common_elements performance -------------------------------------
    import random
    random.seed(42)
    a = list(range(50_000))
    b = list(range(25_000, 75_000))
    check_perf("find_common_elements 50k x 50k fast", lambda: sol.find_common_elements(a, b), 0.5)

    print(f"\nResults: {passed}/{passed + failed} tests passed")
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
