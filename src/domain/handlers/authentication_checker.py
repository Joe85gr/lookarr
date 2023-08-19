from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

from src.domain.config.lookarr_config import LookarrConfig
from src.domain.auth.authentication import Auth
from src.logger import Log


class check_authentication:
    def __init__(self,
                 auth: Auth,
                 config: LookarrConfig):
        self.logger = Log.get_logger(__name__)
        self.auth = auth
        self.config = config

    def __call__(self, func):
        def wrapper(cls, update: Update, context: CallbackContext) -> object:
            user = update.effective_user

            if not self.auth.user_is_authenticated_strict(user.id, self.config):
                self.logger.info(f"unauthorised user {user.id}")
                return ConversationHandler.END
            elif not self.auth.user_is_authenticated(user.id):
                update.message.reply_text(
                    "Well, shit! 😄 seems you're not authenticated! Write /auth <password> to authenticate!")
                return ConversationHandler.END

            return func(cls, update, context)

        return wrapper
