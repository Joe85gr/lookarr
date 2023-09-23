from telegram import Update
from telegram.ext import CallbackContext
from kink import inject

from src.constants import MEDIA_SELECTED, SEASON_SELECTION
from src.domain.checkers.authentication_checker import check_user_is_authenticated
from src.domain.checkers.search_checker import check_search_is_valid
from src.domain.handlers.interfaces.iseries_handler import ISeriesHandler
from src.domain.checkers.conversation_checker import check_conversation
from src.domain.handlers.messages_handler import MessagesHandler
from src.domain.handlers.interfaces.ihandler import IHandler
from src.interface.keyboard import Keyboard
from src.logger import ILogger


@inject
class SeriesHandler(ISeriesHandler):
    def __init__(self,
                 logger: ILogger,
                 media_handler: IHandler,
                 ):
        self._logger = logger
        self._media_handler = media_handler

    @check_user_is_authenticated
    @check_search_is_valid()
    async def search_media(self, update: Update, context: CallbackContext) -> int:
        context.user_data["type"] = "Sonarr"
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
        default_profile_action = self.select_season
        return await self._media_handler.get_quality_profiles(update, context, default_profile_action)

    @check_user_is_authenticated
    @check_conversation(["update_msg", "type"])
    async def set_quality(self, update: Update, context: CallbackContext) -> int:
        query = update.callback_query

        if not context.user_data.get("quality_profile"):
            context.user_data["quality_profile"] = query.data.removeprefix("SonarrQuality: ")

        return await self.select_season(update, context)

    @check_user_is_authenticated
    @check_conversation(["update_msg", "type"])
    async def select_season(self, update: Update, context: CallbackContext) -> int:
        await MessagesHandler.delete_current_and_add_new(context, update, ".. 👀")

        query = update.callback_query

        position = context.user_data["position"]

        if not "seasons" in context.user_data:
            self._set_seasons(context, position)
        else:
            self._update_selected_seasons(query, context)

        seasons = context.user_data["seasons"]

        keyboard = Keyboard.seasons(seasons)

        await MessagesHandler.delete_current_and_add_new(context, update, "Select Season:", keyboard)

        return SEASON_SELECTION

    @check_user_is_authenticated
    @check_conversation(["update_msg", "type"])
    async def add_to_library(self, update: Update, context: CallbackContext) -> int:
        return await self._media_handler.add_to_library(update, context)

    @staticmethod
    def _set_seasons(context: CallbackContext, position: int):
        seasons = context.user_data['results'][position]['seasons']
        seasons = [season for season in seasons if season["seasonNumber"] != 0]
        for season in seasons:
            season["selected"] = False

        context.user_data["seasons"] = seasons

    @staticmethod
    def _update_selected_seasons(query, context: CallbackContext):
        selected_season = query.data.removeprefix("SelectSeason: ")
        if selected_season in ["All", "Unselect"]:
            selected = True if selected_season == "All" else False
            for season in context.user_data["seasons"]:
                season["selected"] = selected
        else:
            for season in context.user_data["seasons"]:
                if str(season["seasonNumber"]) == selected_season:
                    season["selected"] = not season["selected"]
                    break
