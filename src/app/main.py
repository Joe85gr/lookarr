#!/usr/bin/env python
from os import environ

from telegram import InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, ConversationHandler

from src.app.config.config_loader import ConfigLoader
from src.app.interface.buttons import Buttons
from src.domain.authentication import Auth
from src.infrastructure.sqlite import Database
from src.logger import Log
from src.domain.user import UserReply

Database.initialise()
logger = Log.get_logger(__name__)

config = ConfigLoader.set_config()
auth = Auth(Database())
buttons = Buttons()


def search_all_command(update: Update, context: CallbackContext) -> None:
    user = update.effective_user

    if not auth.user_is_authenticated_strict(user.id, config):
        logger.info(f"unauthorised user {user.id}")
        return ConversationHandler.END
    elif not auth.user_is_authenticated(user.id):
        update.message.reply_text(
            "Well, shit! 😄 seems you're not authenticated! Write /auth <password> to authenticate!")
        return ConversationHandler.END

    user_reply = UserReply(update.message.text)

    if not user_reply.is_valid:
        update.message.reply_text('Please choose:')

    keyboard = [
        [buttons.series_button(), buttons.movie_button()],
        [buttons.stop_button()],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)


def auth_command(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    user_reply = UserReply(update.message.text)

    if not auth.user_is_authenticated_strict(user.id, config):
        logger.info(f"unauthorised user {user.id}. Won't reply :D")
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


def button_pressed(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    query.answer()

    query.edit_message_text(text=f"Selected option: {query.data}")


def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Use /start to tests this bot.")


def main() -> None:
    updater = Updater(environ.get("TELEGRAM_BOT_KEY"))

    updater.dispatcher.add_handler(CommandHandler(config.lookarr.search_all_command, search_all_command))
    updater.dispatcher.add_handler(CommandHandler(config.lookarr.search_series_command, search_all_command))
    updater.dispatcher.add_handler(CommandHandler(config.lookarr.search_movie_command, search_all_command))
    updater.dispatcher.add_handler(CallbackQueryHandler(button_pressed))
    updater.dispatcher.add_handler(CommandHandler('help', help_command))
    updater.dispatcher.add_handler(CommandHandler('auth', auth_command))

    # Start bot
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
