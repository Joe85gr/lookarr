from abc import ABC, abstractmethod

from telegram import Update
from telegram.ext import CallbackContext


class IHelpHandler(ABC):
    @staticmethod
    @abstractmethod
    def help(update: Update, context: CallbackContext) -> None:
        """Show help message"""
