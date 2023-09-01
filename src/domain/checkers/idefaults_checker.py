from abc import ABC, abstractmethod

from telegram.ext import CallbackContext

from src.infrastructure.media_server import MediaServer


class IDefaultValuesChecker(ABC):
    @abstractmethod
    def check_defaults(self,
                       profile_name: str,
                       valid_values, media_server: MediaServer,
                       context: CallbackContext
                       ) -> bool:
        """Returns Default Quality Profile"""
