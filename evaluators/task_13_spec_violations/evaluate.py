#!/usr/bin/env python3
"""Evaluator for Task 13: Spec Violations — Token Bucket"""
import sys
import os
import importlib.util

TASK_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        '..', '..', 'tasks', 'task_13_spec_violations')


def load_solution():
    path = os.path.join(TASK_DIR, 'token_bucket.py')
    if not os.path.exists(path):
        print("[FAIL] token_bucket.py not found")
        sys.exit(1)
    spec = importlib.util.spec_from_file_location("token_bucket", path)
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


def main():
    sol = load_solution()
    TB = sol.TokenBucket

    # -- Violation 1: __init__ starts empty instead of full ------------------
    check("fresh bucket starts full",
          lambda: TB(10.0, 1.0).available(),
          10.0)
    check("fresh bucket capacity=5 starts at 5",
          lambda: TB(5.0, 1.0).available(),
          5.0)

    # -- Violation 2: consume zeroes tokens on failure (partial deduction) ---
    def consume_fail_unchanged():
        tb = TB(10.0, 1.0)
        tb.consume(3.0)          # succeeds -> 7.0 remaining
        tb.consume(9.0)          # fails (only 7 available)
        return tb.available()

    check("consume failure leaves tokens unchanged",
          consume_fail_unchanged,
          7.0)

    def consume_fail_returns_false():
        tb = TB(10.0, 1.0)
        return tb.consume(15.0)  # more than capacity

    check("consume failure returns False",
          consume_fail_returns_false,
          False)

    # -- Violation 3: refill does not clamp at capacity ----------------------
    def refill_no_overflow():
        tb = TB(10.0, 2.0)
        tb.consume(5.0)          # 5.0 remaining
        tb.refill(100.0)         # +200 tokens, but capped at 10
        return tb.available()

    check("refill clamps at capacity",
          refill_no_overflow,
          10.0)

    def refill_partial():
        tb = TB(10.0, 2.0)
        tb.consume(8.0)          # 2.0 remaining
        tb.refill(1.0)           # +2 tokens -> 4.0
        return tb.available()

    check("refill partial (within capacity)",
          refill_partial,
          4.0)

    def refill_full_bucket():
        tb = TB(10.0, 2.0)
        tb.refill(5.0)           # bucket already full, should stay at 10
        return tb.available()

    check("refill on full bucket stays at capacity",
          refill_full_bucket,
          10.0)

    # -- Violation 4: reset sets tokens to 0 instead of capacity -------------
    def reset_restores_full():
        tb = TB(10.0, 1.0)
        tb.consume(10.0)         # drain completely
        tb.reset()
        return tb.available()

    check("reset restores to capacity",
          reset_restores_full,
          10.0)

    def reset_capacity_8():
        tb = TB(8.0, 1.0)
        tb.consume(4.0)
        tb.reset()
        return tb.available()

    check("reset with capacity=8 restores to 8",
          reset_capacity_8,
          8.0)

    # -- Integration: all four violations must be fixed together --------------
    def full_scenario():
        tb = TB(10.0, 2.0)
        assert tb.available() == 10.0,  "starts full"
        assert tb.consume(3.0) == True
        assert tb.available() == 7.0
        assert tb.consume(8.0) == False,  "consume failure"
        assert tb.available() == 7.0,    "unchanged after failure"
        tb.refill(1.0)
        assert tb.available() == 9.0,    "partial refill"
        tb.refill(100.0)
        assert tb.available() == 10.0,   "clamped at capacity"
        tb.consume(10.0)
        tb.reset()
        assert tb.available() == 10.0,   "reset to full"
        return True

    check("full scenario passes all spec requirements",
          full_scenario,
          True)

    print(f"\nResults: {passed}/{passed + failed} tests passed")
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
