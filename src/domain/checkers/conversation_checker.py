from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

from src.domain.handlers.stop_handler import stop_handler


class check_conversation:
    def __init__(self, required_keys: list[str]):
        self._required_keys = required_keys

    def __call__(self, func):
        def wrapper(cls, update: Update, context: CallbackContext) -> object:
            query = update.callback_query
            query.answer()

            if stop_handler.lostTrackOfConversation(update, context, self._required_keys):
                return ConversationHandler.END

            return func(cls, update, context)

        return wrapper
