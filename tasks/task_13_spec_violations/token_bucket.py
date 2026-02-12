"""
Task 13: Spec Violations

This TokenBucket implementation deviates from the specification in
instructions.md in several places. Find and fix every violation so
that the class behaves exactly as the spec describes.
"""


class TokenBucket:
    """A token-bucket rate limiter."""

    def __init__(self, capacity, refill_rate):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = 0.0

    def available(self):
        """Return the current token count."""
        return self.tokens

    def consume(self, tokens):
        """Consume tokens if available; return True on success, False on failure."""
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        self.tokens = 0.0
        return False

    def refill(self, elapsed_seconds):
        """Add refill_rate * elapsed_seconds tokens to the bucket."""
        self.tokens += self.refill_rate * elapsed_seconds

    def reset(self):
        """Restore the bucket to its initial state."""
        self.tokens = 0.0
