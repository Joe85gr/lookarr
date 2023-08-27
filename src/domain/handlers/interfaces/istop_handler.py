from abc import ABC

from telegram import Update
from telegram.ext import CallbackContext


class IStopHandler(ABC):
    def stop(self, update: Update, context: CallbackContext) -> None | int:
        """Stop the current conversation"""

    def clear_user_data(self, update: Update, context: CallbackContext, delete_last_message=True):
        """Clear the user data"""

    def lost_track_of_conversation(self, update: Update, context: CallbackContext, required_keys: list[str]) -> bool:
        """Check if bot has lost track of conversation"""
