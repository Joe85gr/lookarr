from abc import ABC

from telegram import Update
from telegram.ext import CallbackContext


class IAuthHandler(ABC):
    def authenticate(self, update: Update, context: CallbackContext) -> None | int:
        """Authenticate user"""
