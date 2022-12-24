from logging import Logger

from telegram import Update, InlineKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler
from src.app.interface.buttons import Buttons
from src.app.config.all_config import Config

from src.domain.authentication import Auth
from src.domain.user import UserReply


class Commands:
    def __init__(
            self,
            logger: Logger,
            auth: Auth,
            config: Config):
        self.logger = logger
        self.auth = auth
        self.buttons = Buttons()
        self.config = config

    def search_all_command(self, update: Update, context: CallbackContext) -> None:
        user = update.effective_user

        if not self.auth.user_is_authenticated_strict(user.id, self.config):
            self.logger.info(f"unauthorised user {user.id}")
            return ConversationHandler.END
        elif not self.auth.user_is_authenticated(user.id):
            update.message.reply_text(
                "Well, shit! 😄 seems you're not authenticated! Write /auth <password> to authenticate!")
            return ConversationHandler.END

        user_reply = UserReply(update.message.text)

        if not user_reply.is_valid:
            update.message.reply_text('Please choose:')

        keyboard = [
            [self.buttons.series_button(), self.buttons.movie_button()],
            [self.buttons.stop_button()],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text('Please choose:', reply_markup=reply_markup)

    def auth_command(self, update: Update, context: CallbackContext) -> None:
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

    def button_pressed(self, update: Update, context: CallbackContext) -> None:
        query = update.callback_query

        query.answer()

        query.edit_message_text(text=f"Selected option: {query.data}")

    def help_command(self, update: Update, context: CallbackContext) -> None:
        update.message.reply_text("Use /start to tests this bot.")
