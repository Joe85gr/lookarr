from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

from src.domain.config.app_config import config
from src.domain.auth.authentication import auth
from src.logger import Log


class check_user_is_authenticated:
    def __init__(self):
        self._logger = Log.get_logger(__name__)
        self._config = config.lookarr

    def __call__(self, func):
        def wrapper(cls, update: Update, context: CallbackContext) -> object:
            user = update.effective_user

            if not auth.user_is_authenticated_strict(user.id, self._config):
                self._logger.info(f"unauthorised user {user.id}")
                return ConversationHandler.END
            elif not auth.user_is_authenticated(user.id):
                update.message.reply_text(
                    "Well, shit! 😄 seems you're not authenticated! Write /auth <password> to authenticate!")
                return ConversationHandler.END

            return func(cls, update, context)

        return wrapper
