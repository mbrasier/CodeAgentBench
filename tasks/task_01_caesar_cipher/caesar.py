def encode(text: str, shift: int) -> str:
    """Encode a string using the Caesar cipher.

    Only alphabetic characters are shifted; all other characters are unchanged.
    Case is preserved. Shifting wraps around the alphabet.
    Negative shifts and shifts > 26 are handled correctly.

    Args:
        text:  The plaintext string to encode.
        shift: Number of positions to shift each letter (may be negative).

    Returns:
        The Caesar-cipher encoded string.

    Examples:
        >>> encode("Hello, World!", 3)
        'Khoor, Zruog!'
        >>> encode("xyz", 3)
        'abc'
    """
    raise NotImplementedError


def decode(text: str, shift: int) -> str:
    """Decode a Caesar-encoded string.

    This is the exact inverse of encode:
        decode(encode(text, shift), shift) == text

    Args:
        text:  The encoded string.
        shift: The shift that was used to encode.

    Returns:
        The original plaintext string.
    """
    raise NotImplementedError
