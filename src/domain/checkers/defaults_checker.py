from src import Logger
from kink import inject
from telegram.ext import CallbackContext

from src.domain.checkers.idefaults_checker import IDefaultValuesChecker
from src.infrastructure.media_server import MediaServer


@inject
class DefaultValuesChecker(IDefaultValuesChecker):
    def __init__(self, logger: Logger):
        self._logger = logger

    def is_valid(self,
                 profile_name: str,
                 profile_name_identifier: str,
                 profile_key_identifier: str,
                 valid_values,
                 media_server: MediaServer,
                 context: CallbackContext
                 ) -> bool:
        default_value = media_server.media_server.defaults[profile_name]

        if default_value:
            match = next((profile for profile in valid_values
                          if profile[profile_name_identifier] == default_value),
                         None)

            if match and profile_key_identifier in match:
                context.user_data[profile_name] = match[profile_key_identifier]
                return True
            else:
                valid_value_names = [profile[profile_name_identifier] for profile in valid_values]
                self._logger.error(f"The Default {profile_name} '{default_value}' is not valid. "
                                   f"Valid values: {valid_value_names}")
        return False
