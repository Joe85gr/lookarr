from telegram import Update
from telegram.ext import CallbackContext
from kink import inject

from src.constants import MEDIA_SELECTED
from src.domain.checkers.authentication_checker import check_user_is_authenticated
from src.domain.checkers.conversation_checker import check_conversation
from src.domain.checkers.search_checker import check_search_is_valid
from src.domain.handlers.interfaces.imovie_handler import IMovieHandler
from src.domain.handlers.interfaces.ihandler import IHandler
from src.logger import ILogger


@inject
class MovieHandler(IMovieHandler):
    def __init__(self,
                 logger: ILogger,
                 media_handler: IHandler
                 ):
        self._logger = logger
        self._media_handler = media_handler

    @check_user_is_authenticated
    @check_search_is_valid()
    async def search_media(self, update: Update, context: CallbackContext) -> int:
        context.user_data["type"] = "Radarr"
        return await self._media_handler.search_media(update, context)

    @check_user_is_authenticated
    @check_conversation(["update_msg", "type"])
    async def get_folders(self, update: Update, context: CallbackContext) -> int:
        default_folder_action = self.get_quality_profiles
        await self._media_handler.get_folders(update, context, default_folder_action)

        return MEDIA_SELECTED

    @check_user_is_authenticated
    @check_conversation(["update_msg", "type"])
    async def get_quality_profiles(self, update: Update, context: CallbackContext) -> int:
        default_profile_action = self.add_to_library
        return await self._media_handler.get_quality_profiles(update, context, default_profile_action)

    async def add_to_library(self, update: Update, context: CallbackContext) -> int:
        query = update.callback_query

        if not context.user_data.get("quality_profile") and query.data.startswith("RadarrQuality"):
            context.user_data["quality_profile"] = query.data.removeprefix("RadarrQuality: ")

        return await self._media_handler.add_to_library(update, context)
