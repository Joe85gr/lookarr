from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

from src.domain.auth.authentication import auth
from src.domain.config.app_config import ConfigLoader
from src.logger import Logger

logger = Logger(__name__)


def check_user_is_authenticated(func):
    def wrapper(cls, update: Update, context: CallbackContext) -> object:
        user = update.effective_user

        if not auth.user_is_authenticated_strict(user.id, ConfigLoader().lookarr):
            logger.info(f"unauthorised user {user.id}")
            return ConversationHandler.END
        elif not auth.user_is_authenticated(user.id):
            update.message.reply_text(
                "Well, shit! 😄 seems you're not authenticated! Write /auth <password> to authenticate!")
            return ConversationHandler.END

        return func(cls, update, context)

    return wrapper
