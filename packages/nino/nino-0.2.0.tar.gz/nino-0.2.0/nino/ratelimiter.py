import datetime
import functools
import time
import typing as t

__all__ = ("Ratelimiter",)


class Ratelimiter:
    def __init__(self, calls: int, time_frame: t.Union[int, float]):
        self.time_frame = datetime.timedelta(seconds=time_frame)
        self.calls = calls
        self.used_calls = 0
        self.last = datetime.datetime.now()

    def _get_remaining(self):
        return self.time_frame - (datetime.datetime.now() - self.last)

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            remaining = self._get_remaining()
            while True:
                if remaining.total_seconds() <= 0:
                    self.used_calls = 0
                    self.last = datetime.datetime.now()

                self.used_calls += 1
                if self.used_calls > self.calls:
                    time.sleep(self.time_frame.seconds)
                return func(*args, **kwargs)

        return wrapper
