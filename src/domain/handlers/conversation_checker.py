from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

from src.domain.config.lookarr_config import LookarrConfig
from src.domain.auth.authentication import Auth
from src.domain.handlers.stop import stop_handler
from src.logger import Log


class check_conversation:
    def __init__(self, required_keys: list[str]):
        self.required_keys = required_keys

    def __call__(self, func):
        def wrapper(cls, update: Update, context: CallbackContext) -> object:
            query = update.callback_query
            query.answer()

            if stop_handler.lostTrackOfConversation(update, context, self.required_keys):
                return ConversationHandler.END

            return func(cls, update, context)

        return wrapper
