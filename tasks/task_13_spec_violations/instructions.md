# Task 13: Spec Violations — Token Bucket

The file `token_bucket.py` implements a `TokenBucket` rate-limiter class.
The implementation **does not conform to the specification below**.
Your task is to read the specification carefully, compare it with the code,
and fix every deviation — without adding new behaviour or changing the API.

## Specification

### `TokenBucket(capacity, refill_rate)`
Creates a new token bucket.

- `capacity` — maximum number of tokens the bucket can hold (float)
- `refill_rate` — tokens added per second when `refill()` is called (float)
- **On construction the bucket starts full** (tokens == capacity).

### `available() -> float`
Returns the current number of tokens in the bucket.

### `consume(tokens) -> bool`
Attempts to consume `tokens` tokens from the bucket.

- If `self.tokens >= tokens`: deduct `tokens`, return `True`.
- If `self.tokens < tokens`: **leave the token count unchanged**, return `False`.
  (No partial deduction on failure.)

### `refill(elapsed_seconds)`
Adds `refill_rate * elapsed_seconds` tokens to the bucket.
The token count must **never exceed `capacity`** after a refill.

### `reset()`
Restores the bucket to its full capacity (tokens == capacity).

## Examples

```python
tb = TokenBucket(10.0, 2.0)
assert tb.available() == 10.0    # starts full

assert tb.consume(3.0) == True
assert tb.available() == 7.0

assert tb.consume(8.0) == False  # not enough tokens
assert tb.available() == 7.0    # unchanged after failure

tb.refill(1.0)                   # +2 tokens -> 9.0
assert tb.available() == 9.0

tb.refill(100.0)                 # would be 209 but clamped to capacity
assert tb.available() == 10.0

tb.consume(10.0)
assert tb.available() == 0.0
tb.reset()
assert tb.available() == 10.0   # reset restores to capacity, not 0
```
