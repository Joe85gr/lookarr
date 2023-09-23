from abc import ABC

from telegram import Update
from telegram.ext import ContextTypes


class IAuthHandler(ABC):
    async def authenticate(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Authenticate user"""
