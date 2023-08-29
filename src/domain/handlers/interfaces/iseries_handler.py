from abc import ABC, abstractmethod

from telegram import Update
from telegram.ext import CallbackContext


class ISeriesHandler(ABC):
    @abstractmethod
    def select_season(self, update: Update, context: CallbackContext):
        """Select season"""

    @abstractmethod
    def set_season(self, update: Update, context: CallbackContext):
        """Set season"""
