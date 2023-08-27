from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler
from telegram.error import BadRequest
from kink import inject

from src.domain.checkers.authentication_checker import check_user_is_authenticated
from src.logger import ILogger


@inject
class StopHandler:
    def __init__(self, logger: ILogger):
        self._logger = logger

    @check_user_is_authenticated
    def stop(self, update, context):
        self.clear_user_data(update, context)

        context.bot.send_message(chat_id=update.effective_message.chat_id, text="Ok, nothing to do for me then 🌝")

        return ConversationHandler.END

    def clear_user_data(self, update: Update, context: CallbackContext, delete_last_message=True):
        msg = update.effective_message

        if delete_last_message:
            try:
                context.bot.delete_message(chat_id=update.effective_message.chat_id, message_id=msg.message_id)
            except BadRequest as e:
                if not e.message.startswith("Message to delete not found"):
                    self._logger.error(f"could not delete message id {msg.message_id}", e)

        items = [item for item in context.user_data]
        [context.user_data.pop(item) for item in items]

    def lost_track_of_conversation(self, update: Update, context: CallbackContext, required_keys: list[str]) -> bool:
        for key in required_keys:
            if not key in context.user_data:
                self._send_lost_track_message(update, context)
                self.clear_user_data(update, context)
                return True

        return False

    @staticmethod
    def _send_lost_track_message(update: Update, context: CallbackContext):
        message = "Sorry, kinda lost track of the conversation.. 😅 try again!"
        context.bot.send_message(chat_id=update.effective_message.chat_id, text=message)


stop_handler = StopHandler()
