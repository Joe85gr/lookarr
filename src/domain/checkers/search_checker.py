from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

from src.domain.handlers.stop_handler import stop_handler
from src.domain.user import UserReply


class check_search_is_valid:
    def __call__(self, func):
        def wrapper(cls, update: Update, context: CallbackContext) -> object:
            user_reply = UserReply(update.message.text)

            if not user_reply.is_valid:
                update.message.reply_text(
                    "Well, I'm unsure what you want me to search..🧐\nwrite /search <search criteria> "
                    "to get some results.")
                stop_handler.clearUserData(update, context)
                return ConversationHandler.END

            context.user_data["reply"] = user_reply.value

            return func(cls, update, context)

        return wrapper
