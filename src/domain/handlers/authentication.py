from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler
from src.domain.config.app_config import config
from src.domain.auth.authentication import auth
from src.domain.user import UserReply
from src.logger import Log


class AuthHandler:
    def __init__(self):
        self.logger = Log.get_logger(__name__)

    def authenticate(self, update: Update, context: CallbackContext) -> None | int:
        user = update.effective_user
        user_reply = UserReply(update.message.text)

        if not auth.user_is_authenticated_strict(user.id, config.lookarr):
            self.logger.info(f"unauthorised user {user.id}. Won't reply :D")
            return ConversationHandler.END
        elif auth.user_is_authenticated(user.id):
            update.message.reply_text(
                text="What you want?? You're already authenticated! Do you like passwords or something 🤣")
        elif not user_reply.is_valid:
            update.message.reply_text(text=f"You need to write /auth <password> 😒 don't make me repeat myself..")
        elif not auth.authenticate_user(user.id, user_reply.value):
            update.message.reply_text(text=f"Sorry pal, wrong password 😝 try again.")
        else:
            update.message.reply_text(text=f"Nice one! You're in buddy 😌")
