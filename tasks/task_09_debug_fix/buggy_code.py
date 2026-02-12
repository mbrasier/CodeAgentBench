"""
buggy_code.py — four functions, each containing exactly one bug.
Find and fix every bug.  Comments marked  # BUG:  point to the problematic lines.
"""

from typing import List


def binary_search(arr: List, target) -> int:
    """Return the index of target in sorted arr, or -1 if not found."""
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid          # BUG: causes infinite loop when target is in the right half
        else:
            right = mid - 1
    return -1


def make_list(item, result=[]) -> List:  # BUG: mutable default argument shared across calls
    """Return a fresh list containing only item."""
    result.append(item)
    return result


def is_palindrome(s: str) -> bool:
    """Return True if s is a palindrome (case-insensitive, ignoring spaces)."""
    cleaned = s.lower().replace(" ", "")
    return cleaned == cleaned[1:]   # BUG: should compare to the reversed string


def max_sliding_window(arr: List[int], k: int) -> List[int]:
    """Return the maximum of each contiguous subarray of length k."""
    result = []
    for i in range(len(arr) - k):   # BUG: off-by-one; last window is never included
        result.append(max(arr[i : i + k]))
    return result
