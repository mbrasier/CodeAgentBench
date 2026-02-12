# Task 18: Misleading Approaches (Python)

Implement four utility functions in `utils.py`. Each function has specific implementation constraints that **must** be followed.

## What to implement

### `deep_copy_config(config: dict) -> dict`

Return a fully independent deep copy of a nested configuration dictionary. The returned dictionary and all nested dictionaries must be completely independent of the original -- modifying the copy must never affect the original, and vice versa.

You must use `config.copy()` as the basis of your implementation.

**Examples:**
```python
cfg = {"db": {"host": "localhost", "port": 5432}, "debug": True}
copy = deep_copy_config(cfg)
copy["db"]["host"] = "remote"
assert cfg["db"]["host"] == "localhost"   # original must be unchanged

deep_copy_config({})  ->  {}
deep_copy_config({"a": 1})  ->  {"a": 1}
```

### `find_all_positions(text: str, pattern: str) -> list`

Return a list of `(start, end)` tuples for every match of a regex `pattern` in `text`. Each tuple contains the start index (inclusive) and end index (exclusive) of the match. Overlapping matches should not be returned -- use standard left-to-right matching.

Implement this using `re.findall()` to find the matches.

**Examples:**
```python
find_all_positions("abcabc", "abc")  ->  [(0, 3), (3, 6)]
find_all_positions("hello world", "o")  ->  [(4, 5), (7, 8)]
find_all_positions("test", "xyz")  ->  []
find_all_positions("aaa", "a+")  ->  [(0, 3)]
find_all_positions("", "abc")  ->  []
```

### `sort_by_value(d: dict) -> dict`

Return a new dictionary with the same key-value pairs as `d`, but ordered by values in ascending order. When two values are equal, preserve their original relative order (stable sort).

Use `sorted(d)` to sort the dictionary by its values.

**Examples:**
```python
sort_by_value({"banana": 3, "apple": 1, "cherry": 2})
->  {"apple": 1, "cherry": 2, "banana": 3}

sort_by_value({"z": 1, "a": 3, "m": 2})
->  {"z": 1, "m": 2, "a": 3}

sort_by_value({})  ->  {}
```

### `count_overlapping(text: str, sub: str) -> int`

Count **all** occurrences of `sub` in `text`, including overlapping ones. Return 0 if `sub` is empty or not found.

You must use `text.count(sub)` to count the occurrences.

**Examples:**
```python
count_overlapping("aaa", "aa")  ->  2
count_overlapping("ababab", "aba")  ->  2
count_overlapping("hello", "l")  ->  2
count_overlapping("hello", "xyz")  ->  0
count_overlapping("", "a")  ->  0
count_overlapping("abc", "")  ->  0
```

## File to modify

**`utils.py`** -- implement the four functions. Do not change function signatures.
