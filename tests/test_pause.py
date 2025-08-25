import time

from autogroceries.pause import pause


def test_pause() -> None:
    @pause(delay=2)
    def f():
        pass

    start_time = time.perf_counter()
    f()
    end_time = time.perf_counter()
    run_time = end_time - start_time
    assert 2 < run_time < 3
