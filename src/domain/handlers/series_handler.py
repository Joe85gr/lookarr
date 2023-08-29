from telegram import Update
from telegram.ext import CallbackContext
from kink import inject

from src.domain.checkers.authentication_checker import check_user_is_authenticated
from src.domain.checkers.conversation_checker import check_conversation
from src.domain.handlers.interfaces.iconversation_handler import IMediaHandler
from src.domain.handlers.interfaces.iseries_handler import ISeriesHandler
from src.domain.handlers.messages_handler import MessagesHandler
from src.interface.keyboard import Keyboard
from src.logger import ILogger


@inject
class SeriesHandler(ISeriesHandler):
    def __init__(self, logger: ILogger, conversation_handler: IMediaHandler):
        self._logger = logger,
        self._conversation_handler = conversation_handler

    @check_user_is_authenticated
    @check_conversation(["update_msg", "type"])
    def select_season(self, update: Update, context: CallbackContext):
        query = update.callback_query

        if not context.user_data.get("quality_profile"):
            context.user_data["quality_profile"] = query.data.removeprefix("SeriesQuality: ")

        position = context.user_data["position"]

        seasons = context.user_data['results'][position]['seasons']
        season_numbers = [int(season["seasonNumber"]) for season in seasons if season["seasonNumber"] != 0]
        context.user_data["season_numbers"] = season_numbers

        keyboard = Keyboard.seasons(season_numbers)

        MessagesHandler.update_message(context, update, "Select Season:", keyboard)

    @check_user_is_authenticated
    @check_conversation(["update_msg", "type"])
    def set_season(self, update: Update, context: CallbackContext):
        query = update.callback_query

        context.user_data["season"] = query.data.removeprefix("SetSeason: ")

        self._conversation_handler.add_to_library(update, context)
