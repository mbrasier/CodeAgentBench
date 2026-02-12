#!/usr/bin/env python3
"""Evaluator for Task 18: Misleading Approaches"""
import sys
import os
import importlib.util

TASK_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        '..', '..', 'tasks', 'task_18_misleading_approaches')


def load_solution():
    path = os.path.join(TASK_DIR, 'utils.py')
    if not os.path.exists(path):
        print("[FAIL] utils.py not found")
        sys.exit(1)
    spec = importlib.util.spec_from_file_location("utils", path)
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


def check_deep_copy_independence(name, make_config):
    """Special check: mutate the copy and verify the original is unchanged."""
    global passed, failed
    try:
        original = make_config()
        sol = load_solution()
        copy = sol.deep_copy_config(original)

        # Mutate the nested dict in the copy
        copy["db"]["host"] = "MUTATED"

        if original["db"]["host"] != "MUTATED":
            print(f"[PASS] {name}")
            passed += 1
        else:
            print(f"[FAIL] {name}: modifying copy changed the original (shallow copy detected)")
            failed += 1
    except NotImplementedError:
        print(f"[FAIL] {name}: not implemented")
        failed += 1
    except Exception as e:
        print(f"[FAIL] {name}: {type(e).__name__}: {e}")
        failed += 1


def main():
    sol = load_solution()

    # ── deep_copy_config: 5 tests ──────────────────────────────────────

    check("deep_copy: empty dict",
          lambda: sol.deep_copy_config({}),
          {})

    check("deep_copy: flat dict",
          lambda: sol.deep_copy_config({"a": 1, "b": 2}),
          {"a": 1, "b": 2})

    check("deep_copy: nested dict values preserved",
          lambda: sol.deep_copy_config({"db": {"host": "localhost", "port": 5432}, "debug": True}),
          {"db": {"host": "localhost", "port": 5432}, "debug": True})

    check_deep_copy_independence(
        "deep_copy: nested dict independence",
        lambda: {"db": {"host": "localhost", "port": 5432}, "debug": True})

    # Deep nesting: three levels
    def check_deep_nesting():
        original = {"a": {"b": {"c": "deep"}}}
        copy = sol.deep_copy_config(original)
        copy["a"]["b"]["c"] = "MUTATED"
        return original["a"]["b"]["c"]

    check("deep_copy: three-level nesting independence",
          check_deep_nesting,
          "deep")

    # ── find_all_positions: 5 tests ────────────────────────────────────

    check("find_positions: basic matches",
          lambda: sol.find_all_positions("abcabc", "abc"),
          [(0, 3), (3, 6)])

    check("find_positions: single char matches",
          lambda: sol.find_all_positions("hello world", "o"),
          [(4, 5), (7, 8)])

    check("find_positions: no matches",
          lambda: sol.find_all_positions("test", "xyz"),
          [])

    check("find_positions: empty text",
          lambda: sol.find_all_positions("", "abc"),
          [])

    # This test catches re.findall -- it returns strings, not tuples
    def check_returns_tuples():
        result = sol.find_all_positions("cat sat cat", "cat")
        if not isinstance(result, list):
            return f"wrong type: {type(result).__name__}"
        if len(result) != 2:
            return f"wrong length: {len(result)}"
        for item in result:
            if not isinstance(item, tuple) or len(item) != 2:
                return f"items must be (start, end) tuples, got {item!r}"
        return result

    check("find_positions: returns list of (start, end) tuples",
          check_returns_tuples,
          [(0, 3), (8, 11)])

    # ── sort_by_value: 5 tests ─────────────────────────────────────────
    # Note: dict equality in Python ignores insertion order, so we compare
    # list(result.items()) to verify correct ordering.

    check("sort_by_value: empty dict",
          lambda: list(sol.sort_by_value({}).items()),
          [])

    check("sort_by_value: single item",
          lambda: list(sol.sort_by_value({"only": 42}).items()),
          [("only", 42)])

    check("sort_by_value: basic sort",
          lambda: list(sol.sort_by_value({"banana": 3, "apple": 1, "cherry": 2}).items()),
          [("apple", 1), ("cherry", 2), ("banana", 3)])

    # This catches sorted(d) -- it sorts by keys alphabetically
    # Keys alphabetically: a, m, z  -> values: 3, 2, 1 (wrong order)
    # By value:            z, m, a  -> values: 1, 2, 3 (correct)
    check("sort_by_value: key order follows values not keys",
          lambda: list(sol.sort_by_value({"z": 1, "a": 3, "m": 2}).items()),
          [("z", 1), ("m", 2), ("a", 3)])

    check("sort_by_value: negative values",
          lambda: list(sol.sort_by_value({"x": 0, "y": -1, "z": 1}).items()),
          [("y", -1), ("x", 0), ("z", 1)])

    # ── count_overlapping: 5 tests ─────────────────────────────────────

    check("count_overlapping: no overlap",
          lambda: sol.count_overlapping("hello", "l"),
          2)

    check("count_overlapping: not found",
          lambda: sol.count_overlapping("hello", "xyz"),
          0)

    check("count_overlapping: empty sub returns 0",
          lambda: sol.count_overlapping("abc", ""),
          0)

    # text.count("aa") returns 1, correct answer is 2
    check("count_overlapping: aaa contains aa twice",
          lambda: sol.count_overlapping("aaa", "aa"),
          2)

    # text.count("aba") returns 1, correct answer is 2
    check("count_overlapping: ababab contains aba twice",
          lambda: sol.count_overlapping("ababab", "aba"),
          2)

    print(f"\nResults: {passed}/{passed + failed} tests passed")
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
