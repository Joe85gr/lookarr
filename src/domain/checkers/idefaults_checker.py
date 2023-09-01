from abc import ABC, abstractmethod

from telegram.ext import CallbackContext

from src.infrastructure.media_server import MediaServer


class IDefaultValuesChecker(ABC):
    @abstractmethod
    def is_valid(self,
                 profile_name: str,
                 profile_name_identifier: str,
                 profile_key_identifier: str,
                 valid_values,
                 media_server: MediaServer,
                 context: CallbackContext
                 ) -> bool:
        """Returns Default Quality Profile"""
