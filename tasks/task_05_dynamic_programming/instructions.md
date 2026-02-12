# Task 05: Dynamic Programming (Python)

Implement three classic dynamic programming problems in `dp.py`.

## Problems

### 1. `fibonacci(n: int) -> int`

Return the n-th Fibonacci number (0-indexed).

```
fibonacci(0)  →  0
fibonacci(1)  →  1
fibonacci(2)  →  1
fibonacci(6)  →  8
fibonacci(10) →  55
```

**Requirement:** Must handle `n` up to at least 1000 efficiently (no naive recursion).
Use memoization or an iterative DP approach.

---

### 2. `longest_common_subsequence(s1: str, s2: str) -> int`

Return the **length** of the longest common subsequence of `s1` and `s2`.

A *subsequence* is formed by deleting some characters (possibly none) without changing the order of the remaining characters.

```
lcs("abcde", "ace")     →  3   ("ace")
lcs("abc",   "abc")     →  3   ("abc")
lcs("abc",   "def")     →  0
lcs("",      "abc")     →  0
lcs("AGGTAB","GXTXAYB") →  4   ("GTAB")
```

---

### 3. `coin_change(coins: list, amount: int) -> int`

Given a list of coin denominations and a target `amount`, return the **minimum number of coins** needed to make up that amount.  Return `-1` if it is impossible.

```
coin_change([1, 5, 10, 25], 36)  →  3   (25 + 10 + 1)
coin_change([1, 2, 5],      11)  →  3   (5 + 5 + 1)
coin_change([2],             3)  →  -1
coin_change([1],             0)  →  0
```

## File to modify

**`dp.py`** — implement `fibonacci`, `longest_common_subsequence`, and `coin_change`.
