# Task 11: Performance Optimization

Your task is to improve the performance of three functions in `slow_functions.py`.
Each function is **correct** but far too slow for large inputs.
You must make them fast enough to pass the timing constraints below — **without
changing the observable behaviour** (same return values, same signatures).

## Functions to Optimise

### `has_duplicates(lst) -> bool`
Returns `True` if the list contains any duplicate values, `False` otherwise.

**Performance requirement:** Must handle a list of 100,000 distinct integers in
under **0.5 seconds**.

### `fibonacci(n) -> int`
Returns the n-th Fibonacci number (0-indexed: `fibonacci(0) == 0`, `fibonacci(1) == 1`).

**Performance requirement:** Must compute `fibonacci(40)` in under **1.0 second**.

### `find_common_elements(a, b) -> list`
Returns a list of elements that appear in both `a` and `b` (order does not matter;
no duplicates in the result).

**Performance requirement:** Must handle two lists of 50,000 integers each in under
**0.5 seconds**.

## Constraints

- Do **not** change the function signatures.
- Do **not** change the return type or semantics.
- You may import from the Python standard library (e.g. `functools`).
- No third-party packages.
