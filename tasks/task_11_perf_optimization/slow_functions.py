"""
Task 11: Performance Optimization

Each function below is correct but too slow for large inputs.
Optimise each one to meet the performance requirements in instructions.md.
Do not change the function signatures or return semantics.
"""


def has_duplicates(lst):
    """Return True if lst contains any duplicate values, False otherwise."""
    for i in range(len(lst)):
        for j in range(i + 1, len(lst)):
            if lst[i] == lst[j]:
                return True
    return False


def fibonacci(n):
    """Return the n-th Fibonacci number (0-indexed)."""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


def find_common_elements(a, b):
    """Return a list of elements that appear in both a and b (no duplicates)."""
    result = []
    for item in a:
        if item in b and item not in result:
            result.append(item)
    return result
