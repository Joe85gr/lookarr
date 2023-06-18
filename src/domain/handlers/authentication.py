from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

from src.domain.config.lookarr_config import LookarrConfig
from src.domain.authentication import Auth
from src.domain.user import UserReply
from src.logger import Log


class AuthHandler:
    def __init__(self,
                 auth: Auth,
                 config: LookarrConfig):
        self.logger = Log.get_logger(__name__)
        self.auth = auth
        self.config = config

    def authenticate(self, update: Update, context: CallbackContext) -> None | int:
        user = update.effective_user
        user_reply = UserReply(update.message.text)

        if not self.auth.user_is_authenticated_strict(user.id, self.config):
            self.logger.info(f"unauthorised user {user.id}. Won't reply :D")
            return ConversationHandler.END
        elif self.auth.user_is_authenticated(user.id):
            update.message.reply_text(
                text="What you want?? You're already authenticated! Do you like passwords or something 🤣")
        elif not user_reply.is_valid:
            update.message.reply_text(text=f"You need to write /auth <password> 😒 don't make me repeat myself..")
        elif not self.auth.authenticate_user(user.id, user_reply.value):
            update.message.reply_text(text=f"Sorry pal, wrong password 😝 try again.")
        else:
            update.message.reply_text(text=f"Nice one! You're in buddy 😌")

    def user_is_authenticated(self, update: Update) -> bool:
        user = update.effective_user

        if not self.auth.user_is_authenticated_strict(user.id, self.config):
            self.logger.info(f"unauthorised user {user.id}")
            return False
        elif not self.auth.user_is_authenticated(user.id):
            update.message.reply_text(
                "Well, shit! 😄 seems you're not authenticated! Write /auth <password> to authenticate!")
            return False

        return True
