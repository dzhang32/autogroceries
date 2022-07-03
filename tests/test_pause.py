import functools
from timeit import default_timer

from autogroceries.utils import pause


# decorator timer used to test pause()
def timer(func):
    """Decorator that times the input function and returns the run time"""

    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = default_timer()
        func(*args, **kwargs)
        end_time = default_timer()
        run_time = end_time - start_time
        return run_time

    return wrapper_timer


def test_pause_default():
    @timer
    @pause
    def f():
        pass

    run_time = f()
    assert 1 < run_time < 2


def test_pause_delay():
    @timer
    @pause(delay=2)
    def f():
        pass

    run_time = f()
    assert 2 < run_time < 3


def test_pause_rand():
    @timer
    @pause(delay=2, rand=2)
    def f():
        pass

    run_time = f()
    assert 2 < run_time < 4
