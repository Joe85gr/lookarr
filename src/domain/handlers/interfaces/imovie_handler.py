from abc import ABC, abstractmethod

from telegram import Update
from telegram.ext import CallbackContext


class IMovieHandler(ABC):
    @abstractmethod
    def get_quality_profiles(self, update: Update, context: CallbackContext):
        """Get quality profiles or set default quality profile"""
    @abstractmethod
    def add_to_library(self, update: Update, context: CallbackContext) -> None | int:
        """Add the selected media to the library"""
