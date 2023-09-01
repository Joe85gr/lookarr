from telegram import Update
from telegram.ext import CallbackContext
from kink import inject

from src.domain.checkers.authentication_checker import check_user_is_authenticated
from src.domain.checkers.conversation_checker import check_conversation
from src.domain.handlers.interfaces.imedia_handler import IMediaHandler
from src.domain.handlers.interfaces.imovie_handler import IMovieHandler
from src.logger import ILogger


@inject
class MovieHandler(IMovieHandler):
    def __init__(self,
                 logger: ILogger,
                 media_handler: IMediaHandler
                 ):
        self._logger = logger
        self._media_handler = media_handler

    @check_user_is_authenticated
    @check_conversation(["update_msg", "type"])
    def get_folders(self, update: Update, context: CallbackContext):
        default_folder_action = self.get_quality_profiles
        self._media_handler.get_folders(update, context, default_folder_action)

    @check_user_is_authenticated
    @check_conversation(["update_msg", "type"])
    def get_quality_profiles(self, update: Update, context: CallbackContext):
        default_profile_action = self.add_to_library
        self._media_handler.get_quality_profiles(update, context, default_profile_action)

    def add_to_library(self, update: Update, context: CallbackContext):
        query = update.callback_query

        if not context.user_data.get("quality_profile") and query.data.startswith("RadarrQuality"):
            context.user_data["quality_profile"] = query.data.removeprefix("RadarrQuality: ")

        self._media_handler.add_to_library(update, context)
