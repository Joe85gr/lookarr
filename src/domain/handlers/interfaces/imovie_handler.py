from abc import ABC, abstractmethod

from telegram import Update
from telegram.ext import CallbackContext


class IMovieHandler(ABC):
    @abstractmethod
    def add_to_library(self, update: Update, context: CallbackContext) -> None | int:
        """Add the selected media to the library"""
