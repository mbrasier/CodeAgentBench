from typing import List


def fibonacci(n: int) -> int:
    """Return the n-th Fibonacci number (0-indexed).

    fibonacci(0) == 0, fibonacci(1) == 1, fibonacci(2) == 1, ...

    Must handle n up to at least 1000 efficiently.
    Do NOT use naive recursion — use memoization or an iterative approach.

    Args:
        n: Non-negative integer index.

    Returns:
        The n-th Fibonacci number.
    """
    raise NotImplementedError


def longest_common_subsequence(s1: str, s2: str) -> int:
    """Return the length of the longest common subsequence of s1 and s2.

    A subsequence is formed by deleting some characters (possibly zero)
    without changing the relative order of the remaining characters.

    Args:
        s1: First string.
        s2: Second string.

    Returns:
        Length of the LCS.

    Examples:
        longest_common_subsequence("abcde", "ace")  == 3
        longest_common_subsequence("abc",   "def")  == 0
    """
    raise NotImplementedError


def coin_change(coins: List[int], amount: int) -> int:
    """Return the minimum number of coins needed to make up amount.

    Each coin denomination in `coins` may be used any number of times.
    Return -1 if the amount cannot be made with the given coins.

    Args:
        coins:  List of positive integer coin denominations.
        amount: Target amount (non-negative integer).

    Returns:
        Minimum number of coins, or -1 if impossible.

    Examples:
        coin_change([1, 5, 10, 25], 36) == 3   (25 + 10 + 1)
        coin_change([2], 3)             == -1
        coin_change([1], 0)             == 0
    """
    raise NotImplementedError
