from src import Logger
from src.domain.checkers.idefaults_checker import IDefaultValuesChecker
from src.domain.handlers.messages_handler import MessagesHandler
from src.infrastructure.folder import Folder
from src.infrastructure.interfaces.imedia_server_factory import IMediaServerFactory
from telegram.ext import CallbackContext
from dacite import from_dict
from telegram import Update

from src.infrastructure.quality_profiles import QualityProfile
from src.interface.keyboard import Keyboard


class DefaultsHandler:
    def __init__(
            self,
            media_server_factory: IMediaServerFactory,
            defaults: IDefaultValuesChecker,
            logger: Logger,
    ):
        self._media_server_factory = media_server_factory
        self._defaults = defaults
        self._logger = logger

    def _get_valid_match(self, media_type):
        media_server = self._media_server_factory.get_media_server(media_type)

        valid_values = media_server.media_server.get_root_folders()
        user_default_value = media_server.media_server.defaults["path"]

        match = next((value for value in valid_values if value["path"] == user_default_value))

        return match if match else valid_values

    def get_folders(self, update: Update, context: CallbackContext, default_is_valid_action):
        media_type = context.user_data["type"]
        media_server = self._media_server_factory.get_media_server(media_type)

        values = self._get_valid_match(media_type)

        if len(values) == 1:
            context.user_data["quality_profile"] = values["id"]
            return default_is_valid_action(update, context)

        folders = media_server.media_server.get_root_folders()

        if len(folders) == 1:
            context.user_data["path"] = folders[0]["path"]
            return default_is_valid_action(update, context)

        results = [from_dict(data_class=Folder, data=folder) for folder in folders]

        keyboard = Keyboard.folders(results, context.user_data["type"])
        MessagesHandler.delete_current_and_add_new(context, update, "Select Path:", keyboard)







    def get_quality_profiles(self, update: Update, context: CallbackContext, default_profile_action):
        media_server = self._media_server_factory.get_media_server(context.user_data["type"])
        valid_values = media_server.media_server.get_quality_profiles()
        default_is_valid = self._defaults.is_valid(profile_name="quality_profile",
                                                   profile_name_identifier="name",
                                                   profile_key_identifier="id",
                                                   valid_values=valid_values,
                                                   media_server=media_server,
                                                   context=context
                                                   )

        if default_is_valid:
            default_profile_action(update, context)
            return

        quality_profiles = media_server.media_server.get_quality_profiles()

        if len(quality_profiles) == 1:
            context.user_data["quality_profile"] = quality_profiles[0]["id"]
            default_profile_action(update, context)
            return

        results = [from_dict(data_class=QualityProfile, data=entry) for entry in quality_profiles]

        keyboard = Keyboard.quality_profiles(results, context.user_data["type"])
        MessagesHandler.delete_current_and_add_new(context, update, "Select Quality Profile:", keyboard)
