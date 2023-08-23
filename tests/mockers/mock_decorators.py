from functools import wraps
from unittest.mock import patch


def mock_decorator(f):
    @wraps(f)
    def decorated_function(cls, update, context):
        return f(cls, update, context)
    return decorated_function


class mock_decorator_class:
    def __init__(self, required_keys: list[str]):
        self._required_keys = required_keys

    def __call__(self, func):
        def wrapper(cls, update, context) -> object:

            return func(cls, update, context)

        return wrapper


def mock_check_user_is_authenticated():
    patch('src.domain.checkers.authentication_checker.check_user_is_authenticated', mock_decorator).start()


def mock_check_check_conversation():
    patch('src.domain.checkers.conversation_checker.check_conversation', mock_decorator_class).start()
