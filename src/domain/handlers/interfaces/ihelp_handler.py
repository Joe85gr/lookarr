from abc import ABC, abstractmethod

from telegram import Update
from telegram.ext import ContextTypes


class IHelpHandler(ABC):
    @staticmethod
    @abstractmethod
    async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Show help message"""
