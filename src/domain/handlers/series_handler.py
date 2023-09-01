from telegram import Update
from telegram.ext import CallbackContext
from kink import inject

from src.domain.checkers.idefaults_checker import IDefaultValuesChecker
from src.infrastructure.interfaces.imedia_server_factory import IMediaServerFactory
from src.domain.checkers.authentication_checker import check_user_is_authenticated
from src.domain.checkers.conversation_checker import check_conversation
from src.domain.handlers.interfaces.imedia_handler import IMediaHandler
from src.domain.handlers.interfaces.iseries_handler import ISeriesHandler
from src.domain.handlers.messages_handler import MessagesHandler
from src.interface.keyboard import Keyboard
from src.logger import ILogger


@inject
class SeriesHandler(ISeriesHandler):
    def __init__(self,
                 media_server_factory: IMediaServerFactory,
                 logger: ILogger,
                 conversation_handler: IMediaHandler,
                 defaults: IDefaultValuesChecker
                 ):
        self._media_server_factory = media_server_factory
        self._logger = logger
        self._conversation_handler = conversation_handler
        self._defaults = defaults

    @check_user_is_authenticated
    @check_conversation(["update_msg", "type"])
    def get_quality_profiles(self, update: Update, context: CallbackContext):
        media_server = self._media_server_factory.get_media_server(context.user_data["type"])

        valid_values = media_server.media_server.get_quality_profiles()
        has_default_profile = self._defaults.check_defaults("quality_profile", valid_values, media_server, context)

        if has_default_profile:
            self.select_season(update, context)
        else:
            self._conversation_handler.get_quality_profiles(update, context)

    @check_user_is_authenticated
    @check_conversation(["update_msg", "type"])
    def set_quality(self, update: Update, context: CallbackContext):
        query = update.callback_query

        if not context.user_data.get("quality_profile"):
            context.user_data["quality_profile"] = query.data.removeprefix("SonarrQuality: ")

        self.select_season(update, context)

    @check_user_is_authenticated
    @check_conversation(["update_msg", "type"])
    def select_season(self, update: Update, context: CallbackContext):
        MessagesHandler.delete_current_and_add_new(context, update, ".. 👀")

        query = update.callback_query

        position = context.user_data["position"]

        if not "seasons" in context.user_data:
            self._set_seasons(context, position)
        else:
            self._update_selected_seasons(query, context)

        seasons = context.user_data["seasons"]

        keyboard = Keyboard.seasons(seasons)

        MessagesHandler.delete_current_and_add_new(context, update, "Select Season:", keyboard)

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
