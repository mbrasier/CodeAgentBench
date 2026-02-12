#!/usr/bin/env python3
"""Evaluator for Task 15: Decorator Pitfalls"""
import sys
import os
import importlib.util

TASK_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        '..', '..', 'tasks', 'task_15_decorator_pitfalls')


def load_solution():
    path = os.path.join(TASK_DIR, 'decorators.py')
    if not os.path.exists(path):
        print("[FAIL] decorators.py not found")
        sys.exit(1)
    spec = importlib.util.spec_from_file_location("decorators", path)
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


def check_raises(name, fn, exc_type):
    global passed, failed
    try:
        fn()
        print(f"[FAIL] {name}: expected {exc_type.__name__}, got no exception")
        failed += 1
    except exc_type:
        print(f"[PASS] {name}")
        passed += 1
    except Exception as e:
        print(f"[FAIL] {name}: expected {exc_type.__name__}, got {type(e).__name__}: {e}")
        failed += 1


def main():
    sol = load_solution()

    # -- logged: must preserve __name__ and __doc__ --------------------------
    # Bug: missing @functools.wraps(func)

    @sol.logged
    def greet(name):
        """Say hello."""
        return f"Hello, {name}"

    check("logged preserves __name__",
          lambda: greet.__name__,
          'greet')
    check("logged preserves __doc__",
          lambda: greet.__doc__,
          'Say hello.')
    check("logged still calls the function",
          lambda: greet("world"),
          "Hello, world")

    # -- retry: must preserve __name__ and __doc__ ---------------------------
    # Bug: missing @functools.wraps(func) on inner wrapper

    @sol.retry(3)
    def flaky():
        """Might fail."""
        return 99

    check("retry preserves __name__",
          lambda: flaky.__name__,
          'flaky')
    check("retry preserves __doc__",
          lambda: flaky.__doc__,
          'Might fail.')

    # retry: fails-then-succeeds
    def make_flaky_then_ok(fail_times):
        attempts = [0]

        @sol.retry(5)
        def fn():
            """Attempt counter."""
            attempts[0] += 1
            if attempts[0] <= fail_times:
                raise ValueError("not yet")
            return attempts[0]

        return fn

    check("retry succeeds after 2 failures",
          lambda: make_flaky_then_ok(2)(),
          3)

    # retry: all attempts fail -> raises
    def all_fail():
        attempts = [0]

        @sol.retry(3)
        def fn():
            attempts[0] += 1
            raise RuntimeError("always fails")

        fn()

    check_raises("retry raises after all attempts fail", all_fail, RuntimeError)

    # -- make_multipliers: late-binding closure bug --------------------------
    # Bug: lambda x: x * i captures i by reference (all see final i=4)

    def test_multipliers():
        fns = sol.make_multipliers()
        return (fns[0](10), fns[2](10), fns[4](10))

    check("make_multipliers fns[0](10) == 0",
          lambda: sol.make_multipliers()[0](10),
          0)
    check("make_multipliers fns[2](10) == 20",
          lambda: sol.make_multipliers()[2](10),
          20)
    check("make_multipliers fns[4](10) == 40",
          lambda: sol.make_multipliers()[4](10),
          40)
    check("make_multipliers all five values",
          lambda: [sol.make_multipliers()[i](10) for i in range(5)],
          [0, 10, 20, 30, 40])

    # -- timed: mutable default argument shared across all decorated fns -----
    # Bug: _registry=[] default is shared; each decoration should get its own list

    @sol.timed
    def fast_fn():
        pass

    @sol.timed
    def slow_fn():
        pass

    fast_fn()
    fast_fn()
    slow_fn()

    check("timed: fast_fn has 2 call times",
          lambda: len(fast_fn.call_times),
          2)
    check("timed: slow_fn has 1 call time",
          lambda: len(slow_fn.call_times),
          1)
    check("timed: fast_fn and slow_fn have separate lists",
          lambda: fast_fn.call_times is not slow_fn.call_times,
          True)
    check("timed: call_times contains floats",
          lambda: all(isinstance(t, float) for t in fast_fn.call_times),
          True)

    print(f"\nResults: {passed}/{passed + failed} tests passed")
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
