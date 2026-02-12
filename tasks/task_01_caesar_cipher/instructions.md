# Task 01: Caesar Cipher (Python)

Implement the Caesar cipher in `caesar.py`.

## Background

The Caesar cipher shifts each letter in a string by a fixed number of positions in the alphabet. It is one of the oldest and simplest encryption schemes.

## What to implement

### `encode(text: str, shift: int) -> str`

Encode a string using the Caesar cipher.

**Rules:**
- Only alphabetic characters (`a-z`, `A-Z`) are shifted; digits, spaces, punctuation, and other characters pass through unchanged.
- Case is preserved: uppercase stays uppercase, lowercase stays lowercase.
- Shifting wraps around: shifting `'z'` by 1 gives `'a'`; shifting `'Z'` by 1 gives `'A'`.
- Negative shifts and shifts larger than 26 must work correctly.

**Examples:**
```
encode("Hello, World!", 3)  →  "Khoor, Zruog!"
encode("xyz", 3)            →  "abc"
encode("ABC", 1)            →  "BCD"
encode("Hello", 0)          →  "Hello"
encode("Hello", 26)         →  "Hello"
encode("DEF", -3)           →  "ABC"
encode("a", 27)             →  "b"
```

### `decode(text: str, shift: int) -> str`

Decode a Caesar-encoded string. Must satisfy:

```python
decode(encode(text, shift), shift) == text   # for all text and shift
```

## File to modify

**`caesar.py`** — implement the `encode` and `decode` functions. Do not change function signatures.
