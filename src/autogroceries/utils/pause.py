import functools
import time
import random


def pause(_func=None, *, delay=1, rand=1):
    def decorator_pause(func):
        @functools.wraps(func)
        def wrapper_pause(*args, **kwargs):
            time.sleep(delay + random.uniform(0, rand))
            return func(*args, **kwargs)
        return wrapper_pause

    if _func is None:
        return decorator_pause
    else:
        return decorator_pause(_func)
