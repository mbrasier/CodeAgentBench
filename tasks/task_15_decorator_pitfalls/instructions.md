# Task 15: Python Decorator Pitfalls

The file `decorators.py` contains four decorator/closure utilities.
Each has **one Python-specific defect**. Your task is to find and fix
every defect so the utilities behave as described below.

There are no hint comments in the code. Read the docstrings, study
the implementations, and use your knowledge of Python decorator and
closure semantics to locate each bug.

## Utilities

### `logged(func)` — decorator
Wraps `func` so that every call prints `"Calling <name>"` (using the
wrapped function's name) before delegating to the original.

**Requirement:** The decorated function must preserve the original
function's `__name__` and `__doc__` attributes.

```python
@logged
def greet(name):
    """Say hello."""
    return f"Hello, {name}"

assert greet.__name__ == 'greet'
assert greet.__doc__ == 'Say hello.'
```

### `retry(n)` — decorator factory
Returns a decorator that retries the wrapped function up to `n` times
on exception. After `n` failed attempts, re-raises the last exception.

**Requirement:** The decorated function must preserve the original
function's `__name__` and `__doc__` attributes.

```python
@retry(3)
def flaky():
    """Might fail."""
    ...

assert flaky.__name__ == 'flaky'
assert flaky.__doc__ == 'Might fail.'
```

### `make_multipliers()` — closure factory
Returns a list of 5 functions where `fns[i](x)` returns `x * i`.

```python
fns = make_multipliers()
assert fns[0](10) == 0    # multiply by 0
assert fns[2](10) == 20   # multiply by 2
assert fns[4](10) == 40   # multiply by 4
```

### `timed(func)` — decorator
Wraps `func` to record the elapsed time of each call.
Each decorated function stores its own call times in an attribute
`call_times` (a list of floats, one per call).

**Requirement:** Two separately decorated functions must have **independent**
`call_times` lists — they must not share the same list.

```python
@timed
def fast(): pass

@timed
def slow(): pass

fast()
fast()
slow()

assert len(fast.call_times) == 2
assert len(slow.call_times) == 1
```
