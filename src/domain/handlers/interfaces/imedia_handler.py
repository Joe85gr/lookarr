from abc import ABC, abstractmethod

from telegram import Update
from telegram.ext import CallbackContext


class IMediaHandler(ABC):
    @abstractmethod
    def get_folders(self, update: Update, context: CallbackContext):
        """Get available library folders"""

    @abstractmethod
    def get_quality_profiles(self, update: Update, context: CallbackContext):
        """Get available quality profiles"""

    @abstractmethod
    def add_to_library(self, update: Update, context: CallbackContext):
        """Add media to library"""
