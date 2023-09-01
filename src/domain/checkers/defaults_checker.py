from src import ILogger
from kink import inject
from telegram.ext import CallbackContext

from src.domain.checkers.idefaults_checker import IDefaultValuesChecker
from src.infrastructure.media_server import MediaServer


@inject
class DefaultValuesChecker(IDefaultValuesChecker):
    def __init__(self, logger: ILogger):
        self._logger = logger

    def check_defaults(self,
                       profile_name: str,
                       valid_values, media_server: MediaServer,
                       context: CallbackContext
        ) -> bool:
        default_value = media_server.media_server.defaults[profile_name]

        if default_value:
            match = next((profile for profile in valid_values if profile['name'] == default_value), None)

            if match and "id" in match:
                context.user_data[profile_name] = match["id"]
                return True
            else:
                valid_value_names = [profile['name'] for profile in valid_values]
                self._logger.error(f"The Default {profile_name} '{default_value}' is not valid. "
                                   f"Valid values: {valid_value_names}")
        return False
