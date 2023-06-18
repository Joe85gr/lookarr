from telegram import Update
from telegram.ext import CallbackContext


class HelpHandler:
    @staticmethod
    def help(update: Update, context: CallbackContext) -> None:
        update.message.reply_text("Use /start to tests this bot.")
