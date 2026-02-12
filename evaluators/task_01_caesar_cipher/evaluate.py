#!/usr/bin/env python3
"""Evaluator for Task 01: Caesar Cipher"""
import sys
import os
import importlib.util

TASK_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        '..', '..', 'tasks', 'task_01_caesar_cipher')


def load_solution():
    path = os.path.join(TASK_DIR, 'caesar.py')
    if not os.path.exists(path):
        print("[FAIL] caesar.py not found")
        sys.exit(1)
    spec = importlib.util.spec_from_file_location("caesar", path)
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

    check("encode lowercase",        lambda: sol.encode("hello", 3),                    "khoor")
    check("encode mixed case",       lambda: sol.encode("Hello, World!", 3),            "Khoor, Zruog!")
    check("encode wrap lower",       lambda: sol.encode("xyz", 3),                      "abc")
    check("encode wrap upper",       lambda: sol.encode("XYZ", 3),                      "ABC")
    check("encode preserves spaces", lambda: sol.encode("hello world", 1),              "ifmmp xpsme")
    check("encode preserves digits", lambda: sol.encode("abc123", 1),                   "bcd123")
    check("encode shift 0",          lambda: sol.encode("Hello, World!", 0),            "Hello, World!")
    check("encode shift 26",         lambda: sol.encode("Hello", 26),                   "Hello")
    check("encode negative shift",   lambda: sol.encode("DEF", -3),                     "ABC")
    check("encode shift > 26",       lambda: sol.encode("a", 27),                       "b")
    check("encode only punctuation", lambda: sol.encode("!@#$%", 10),                   "!@#$%")
    check("encode empty string",     lambda: sol.encode("", 5),                         "")
    check("decode basic",            lambda: sol.decode("Khoor, Zruog!", 3),            "Hello, World!")
    check("decode round-trip",       lambda: sol.decode(sol.encode("Hi there!", 7), 7), "Hi there!")
    check("decode rot13 round-trip", lambda: sol.decode(sol.encode("Python 3!", 13), 13), "Python 3!")

    print(f"\nResults: {passed}/{passed + failed} tests passed")
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
