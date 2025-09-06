import functools
import random
import time
from typing import Callable


def delay(_func=None, *, delay: int = 2) -> Callable:
    """
    Decorator that adds a random length delay before executing a function.

    Intended to emulate human-like behaviour during browser interaction to avoid bot
    detection.
    """

    def decorator_delay(func):
        @functools.wraps(func)
        def wrapper_delay(*args, **kwargs):
            # Add a random delay (up to 0.5 seconds) to emulate a human.
            time.sleep(delay + random.uniform(0, 0.5))
            return func(*args, **kwargs)

        return wrapper_delay

    if _func is None:
        return decorator_delay
    else:
        return decorator_delay(_func)
