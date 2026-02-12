from typing import Dict, List, Tuple


def deep_copy_config(config: dict) -> dict:
    """Return a fully independent deep copy of a nested configuration dictionary.

    The returned dictionary and all nested dictionaries must be completely
    independent of the original -- modifying the copy must never affect
    the original, and vice versa.

    Args:
        config: A nested dictionary to deep copy.

    Returns:
        A new dictionary that is a deep copy of the input.

    Examples:
        >>> cfg = {"db": {"host": "localhost", "port": 5432}, "debug": True}
        >>> copy = deep_copy_config(cfg)
        >>> copy["db"]["host"] = "remote"
        >>> cfg["db"]["host"]
        'localhost'
    """
    raise NotImplementedError


def find_all_positions(text: str, pattern: str) -> List[Tuple[int, int]]:
    """Return a list of (start, end) tuples for every regex match of pattern in text.

    Each tuple contains the start index (inclusive) and end index (exclusive)
    of the match.

    Args:
        text:    The string to search.
        pattern: A regular expression pattern.

    Returns:
        A list of (start, end) tuples for each match.

    Examples:
        >>> find_all_positions("abcabc", "abc")
        [(0, 3), (3, 6)]
        >>> find_all_positions("hello world", "o")
        [(4, 5), (7, 8)]
    """
    raise NotImplementedError


def sort_by_value(d: dict) -> dict:
    """Return a new dictionary ordered by values in ascending order.

    When two values are equal, preserve their original relative order
    (stable sort).

    Args:
        d: A dictionary with comparable values.

    Returns:
        A new dictionary sorted by values ascending.

    Examples:
        >>> sort_by_value({"banana": 3, "apple": 1, "cherry": 2})
        {'apple': 1, 'cherry': 2, 'banana': 3}
    """
    raise NotImplementedError


def count_overlapping(text: str, sub: str) -> int:
    """Count all occurrences of sub in text, including overlapping ones.

    Return 0 if sub is empty or not found.

    Args:
        text: The string to search in.
        sub:  The substring to count.

    Returns:
        The number of (possibly overlapping) occurrences.

    Examples:
        >>> count_overlapping("aaa", "aa")
        2
        >>> count_overlapping("ababab", "aba")
        2
    """
    raise NotImplementedError
