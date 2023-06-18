from src.domain.handlers.authentication import AuthHandler
from src.logger import Log
from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler


class StopHandler:
    def __init__(
            self,
            auth_handler: AuthHandler
    ):
        self.auth_handler = auth_handler
        self.logger = Log.get_logger(__name__)

    def stop(self, update, context):
        self.auth_handler.check_if_auth(update)

        self.clearUserData(update, context)

        context.bot.send_message(chat_id=update.effective_message.chat_id, text="Ok, nothing to do for me then 🌝")

        return ConversationHandler.END

    def clearUserData(self, update: Update, context: CallbackContext, delete_last_message=True):
        msg = update.effective_message

        if delete_last_message:
            try:
                context.bot.delete_message(chat_id=update.effective_message.chat_id, message_id=msg.message_id)
            except Exception as e:
                if not e.message.startswith("Message to delete not found"):
                    self.logger.error(f"could not delete message id {msg.message_id}", e)

        items = [item for item in context.user_data]
        [context.user_data.pop(item) for item in items]
