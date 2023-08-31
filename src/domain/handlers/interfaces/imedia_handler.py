from abc import ABC, abstractmethod

from telegram import Update
from telegram.ext import CallbackContext


class IMediaHandler(ABC):
    @abstractmethod
    def start_search(self, update: Update, context: CallbackContext) -> None | int:
        """Search for a movie or tv show"""

    @abstractmethod
    def change_option(self, update: Update, context: CallbackContext) -> None | int:
        """Change the current option"""

    @abstractmethod
    def get_folders(self, update: Update, context: CallbackContext) -> None | int:
        """Get the available folders"""

    @abstractmethod
    def get_quality_profiles(self, update: Update, context: CallbackContext) -> None | int:
        """Get the available quality profiles"""

    @abstractmethod
    def add_to_library(self, update: Update, context: CallbackContext) -> None | int:
        """Add the selected media to the library"""

    @abstractmethod
    def confirm_delete(self, update: Update, context: CallbackContext) -> None | int:
        """Confirm the deletion of the selected media"""

    @abstractmethod
    def delete(self, update: Update, context: CallbackContext) -> None | int:
        """Delete the selected media"""

    @abstractmethod
    def search_media(self, update: Update, context: CallbackContext) -> None | int:
        """Search for a movie or tv show"""
