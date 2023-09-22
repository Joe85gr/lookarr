from functools import wraps
from time import time

from src.logger import Logger
from kink import inject


@inject
class Timer:
    def __init__(self, logger: Logger):
        self._logger = logger

    def __call__(self, func):
        @wraps(func)
        def wrap_func(*args: object, **kwargs: object) -> object:
            t1 = time()
            result = func(*args, **kwargs)
            t2 = time()
            self._logger.info(f'{func.__name__!r} executed in {(t2 - t1):.3f}s')
            return result
        return wrap_func
