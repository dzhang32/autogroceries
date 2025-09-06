import time

from autogroceries.delay import delay


def test_delay() -> None:
    """
    Test that functions are delayed correctly.
    """

    @delay(delay=2)
    def f():
        pass

    start_time = time.perf_counter()
    f()
    end_time = time.perf_counter()
    run_time = end_time - start_time
    assert 2 < run_time < 3
