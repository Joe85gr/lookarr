from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

from src.domain.handlers.stop_handler import stop_handler


class check_conversation:
    def __init__(self, required_keys: list[str]):
        self._required_keys = required_keys

    def __call__(self, func):
        @answer_query()
        def wrapper(cls, update: Update, context: CallbackContext) -> object:
            if stop_handler.lost_track_of_conversation(update, context, self._required_keys):
                return ConversationHandler.END

            return func(cls, update, context)

        return wrapper


class answer_query:
    def __call__(self, func):
        def wrapper(cls, update: Update, context: CallbackContext) -> object:
            try:
                update.callback_query.answer()
            except AttributeError:
                pass

            return func(cls, update, context)

        return wrapper
