# Task 09: Debug & Fix (Python)

Find and fix **four bugs** in `buggy_code.py`.  Each function has exactly one bug.

## Functions to fix

### `binary_search(arr, target) -> int`
Should return the index of `target` in the sorted list `arr`, or `-1` if not found.
The current implementation has an off-by-one error that can cause an infinite loop.

### `make_list(item, result=[]) -> list`
Should return a brand-new list containing only `item` each time it is called.
The current implementation has a classic Python pitfall that causes state to bleed between calls.

### `is_palindrome(s: str) -> bool`
Should return `True` if `s` is a palindrome after lowercasing and stripping spaces.
The current string comparison is incorrect.

### `max_sliding_window(arr, k) -> list`
Should return a list of the maximum value in each contiguous subarray of size `k`.
The current loop range is off by one, causing the last window to be missed.

## Rules

- Fix **only the bugs** — do not rewrite logic that is already correct.
- Do not change function signatures.
- The file contains comments marking each bug with `# BUG:`.

## File to modify

**`buggy_code.py`**
