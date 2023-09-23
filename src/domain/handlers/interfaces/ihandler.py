from abc import ABC, abstractmethod

from telegram import Update
from telegram.ext import CallbackContext, ContextTypes


class IHandler(ABC):
    @abstractmethod
    async def start_search(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Search for a movie or tv show"""

    @abstractmethod
    async def change_option(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Change the current option"""

    @abstractmethod
    def get_folders(self, update: Update, context: CallbackContext, default_folder_action):
        """Get the available folders"""

    @abstractmethod
    async def get_quality_profiles(self, update: Update, context: CallbackContext, default_profile_action):
        """Get the available quality profiles"""

    @abstractmethod
    async def add_to_library(self, update: Update, context: CallbackContext) -> int:
        """Add the selected media to the library"""

    @abstractmethod
    async def confirm_delete(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Confirm the deletion of the selected media"""

    @abstractmethod
    async def delete(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Delete the selected media"""

    @abstractmethod
    async def search_media(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Search for a movie or tv show"""
