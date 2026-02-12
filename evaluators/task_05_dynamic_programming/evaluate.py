#!/usr/bin/env python3
"""Evaluator for Task 05: Dynamic Programming"""
import sys
import os
import importlib.util
import time

TASK_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        '..', '..', 'tasks', 'task_05_dynamic_programming')


def load_solution():
    path = os.path.join(TASK_DIR, 'dp.py')
    if not os.path.exists(path):
        print("[FAIL] dp.py not found")
        sys.exit(1)
    spec = importlib.util.spec_from_file_location("dp", path)
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

    # ── fibonacci ────────────────────────────────────────────────────────────
    check("fib(0)",  lambda: sol.fibonacci(0),  0)
    check("fib(1)",  lambda: sol.fibonacci(1),  1)
    check("fib(2)",  lambda: sol.fibonacci(2),  1)
    check("fib(6)",  lambda: sol.fibonacci(6),  8)
    check("fib(10)", lambda: sol.fibonacci(10), 55)
    check("fib(20)", lambda: sol.fibonacci(20), 6765)

    # Performance: fib(1000) must finish quickly
    try:
        t0 = time.time()
        result = sol.fibonacci(1000)
        elapsed = time.time() - t0
        # Known value: fib(1000) is a 209-digit number
        expected_mod = 849228950
        if elapsed > 2.0:
            print(f"[FAIL] fib(1000) performance: took {elapsed:.2f}s (must be < 2s)")
            global failed
            failed += 1
        elif result % (10 ** 9) != expected_mod:
            print(f"[FAIL] fib(1000) value: last 9 digits should be {expected_mod}, got {result % (10**9)}")
            failed += 1
        else:
            print(f"[PASS] fib(1000) correct and fast ({elapsed*1000:.1f}ms)")
            global passed
            passed += 1
    except NotImplementedError:
        print("[FAIL] fib(1000): not implemented")
        failed += 1
    except Exception as e:
        print(f"[FAIL] fib(1000): {type(e).__name__}: {e}")
        failed += 1

    # ── longest_common_subsequence ───────────────────────────────────────────
    lcs = sol.longest_common_subsequence
    check("lcs identical",       lambda: lcs("abc", "abc"),       3)
    check("lcs no common",       lambda: lcs("abc", "def"),       0)
    check("lcs empty s1",        lambda: lcs("", "abc"),          0)
    check("lcs empty both",      lambda: lcs("", ""),             0)
    check("lcs ace in abcde",    lambda: lcs("abcde", "ace"),     3)
    check("lcs AGGTAB/GXTXAYB", lambda: lcs("AGGTAB", "GXTXAYB"), 4)
    check("lcs subsequence",     lambda: lcs("ABCBDAB", "BDCAB"), 4)

    # ── coin_change ──────────────────────────────────────────────────────────
    cc = sol.coin_change
    check("coin_change amount 0",       lambda: cc([1, 5], 0),           0)
    check("coin_change impossible",     lambda: cc([2], 3),              -1)
    check("coin_change simple",         lambda: cc([1, 2, 5], 11),       3)
    check("coin_change exact coin",     lambda: cc([1, 5, 10, 25], 25),  1)
    check("coin_change greedy wrong",   lambda: cc([1, 3, 4], 6),        2)   # 3+3, not 4+1+1
    check("coin_change us coins",       lambda: cc([1, 5, 10, 25], 36),  3)   # 25+10+1

    print(f"\nResults: {passed}/{passed + failed} tests passed")
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
