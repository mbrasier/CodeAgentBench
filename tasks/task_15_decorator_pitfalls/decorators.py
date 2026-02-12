"""
Task 15: Decorator Pitfalls

Each utility below has one Python-specific defect.
Fix every defect so the utilities behave according to instructions.md.
"""
import functools
import time


def logged(func):
    """Decorator: prints "Calling <name>" before each call."""
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper


def retry(n):
    """Decorator factory: retry func up to n times on exception."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            last_err = None
            for _ in range(n):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_err = e
            raise last_err
        return wrapper
    return decorator


def make_multipliers():
    """Return a list of 5 functions where fns[i](x) == x * i."""
    fns = []
    for i in range(5):
        fns.append(lambda x: x * i)
    return fns


def timed(func, _registry=[]):
    """Decorator: records elapsed time of each call in func.call_times."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        t0 = time.time()
        result = func(*args, **kwargs)
        _registry.append(time.time() - t0)
        return result
    wrapper.call_times = _registry
    return wrapper
