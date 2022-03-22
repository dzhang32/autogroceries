import functools
import time
import random


def pause(_func=None, *, delay=1, rand=1):
    """Decorator that pauses for a random-ish interval before executing function

    Used to delay the execution of functions that use Selenium by random-ish
    intervals to 1. seem more human-like and 2. avoid being blocked a website
    for too many requests within a set time frame.

    Parameters
    ----------
    _func : function, default None
        Function to be wrapped by decorator.
    delay : float, default 1
        Fixed duration in seconds to pause before function call.
    rand : float, default 1
        Random time interval to add to fixed delay, generated using
        random.uniform(0, rand).
    """

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
