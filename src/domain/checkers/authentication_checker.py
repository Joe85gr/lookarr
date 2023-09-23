from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler
from kink import inject

from src.domain.auth.interfaces.iauthentication import IAuth
from src.logger import ILogger


def check_user_is_authenticated(func):
    @inject
    async def wrapper(cls, update: Update, context: CallbackContext, auth: IAuth, logger: ILogger) -> object:
        user = update.effective_user

        if not auth.user_is_authenticated_strict(user.id):
            logger.info(f"unauthorised user {user.id}")
            return ConversationHandler.END
        elif not auth.user_is_authenticated(user.id):
            await update.message.reply_text("Well, shit! 😄 seems you're not authenticated! "
                                            "Write /auth <password> to authenticate!")
            return ConversationHandler.END

        return await func(cls, update, context)

    return wrapper
