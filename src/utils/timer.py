from time import time, sleep


class Timer:
    def __init__(self, text):
        self.text = text

    def __call__(self, func):
        def wrap_func(*args: object, **kwargs: object) -> object:
            t1 = time()
            sleep(1)
            result = func(*args, **kwargs)
            t2 = time()
            print(f'{self.text}: {func.__name__!r} executed in {(t2 - t1):.3f}s')
            return result
        return wrap_func
