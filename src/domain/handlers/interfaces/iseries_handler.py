from abc import ABC, abstractmethod

from telegram import Update
from telegram.ext import CallbackContext


class ISeriesHandler(ABC):
    @abstractmethod
    def get_quality_profiles(self, update: Update, context: CallbackContext):
        """Get quality profiles or set default quality profile"""

    @abstractmethod
    def set_quality(self, update: Update, context: CallbackContext):
        """Set quality"""

    @abstractmethod
    def select_season(self, update: Update, context: CallbackContext):
        """Select season"""
