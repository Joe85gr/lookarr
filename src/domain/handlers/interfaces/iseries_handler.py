from abc import ABC, abstractmethod

from telegram import Update
from telegram.ext import CallbackContext

from src.domain.handlers.interfaces.imedia_handler import IMediaHandler


class ISeriesHandler(IMediaHandler, ABC):
    """Series handler interface"""

    @abstractmethod
    def set_quality(self, update: Update, context: CallbackContext):
        """Set quality"""

    @abstractmethod
    def select_season(self, update: Update, context: CallbackContext):
        """Select season"""
