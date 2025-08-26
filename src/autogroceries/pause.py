import functools
import random
import time
from typing import Callable


def pause(_func=None, *, delay: int = 2) -> Callable:
    def decorator_pause(func):
        @functools.wraps(func)
        def wrapper_pause(*args, **kwargs):
            # Add a random delay (up to 0.5 seconds) to emulate a human.
            time.sleep(delay + random.uniform(0, 0.5))
            return func(*args, **kwargs)

        return wrapper_pause

    if _func is None:
        return decorator_pause
    else:
        return decorator_pause(_func)
