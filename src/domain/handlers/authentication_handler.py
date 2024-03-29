from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler
from kink import inject

from src.domain.auth.interfaces.iauthentication import IAuth
from src.domain.config.app_config import Config
from src.domain.handlers.interfaces.iauthentication_handler import IAuthHandler
from src.domain.user import UserReply
from src.logger import Logger


@inject
class AuthHandler(IAuthHandler):
    def __init__(self, auth: IAuth, logger: Logger, config: Config):
        self._logger = logger
        self._config = config
        self._auth = auth

    async def authenticate(self, update: Update, context: CallbackContext) -> int:
        user = update.effective_user

        user_reply = UserReply(update.message.text)

        if not self._auth.user_is_authenticated_strict(user.id):
            self._logger.info(f"unauthorised user {user.id}. Won't reply :D")
        elif self._auth.user_is_authenticated(user.id):
            await update.message.reply_text(
                text="What you want?? You're already authenticated! Do you like passwords or something 🤣")
        elif not user_reply.is_valid:
            await update.message.reply_text(text=f"You need to write /auth <password> 😒 don't make me repeat myself..")
        elif not self._auth.authenticate_user(user.id, user_reply.value):
            await update.message.reply_text(text=f"Sorry pal, wrong password 😝 try again.")
        else:
            await update.message.delete()
            await update.message.reply_text(text=f"Nice one! You're in buddy 😌")

        return ConversationHandler.END

