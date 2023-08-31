from telegram import Update
from telegram.ext import CallbackContext
from kink import inject

from src.domain.handlers.interfaces.imedia_handler import IMediaHandler
from src.domain.handlers.interfaces.imovie_handler import IMovieHandler
from src.logger import ILogger


@inject
class MovieHandler(IMovieHandler):
    def __init__(self, logger: ILogger, conversation_handler: IMediaHandler):
        self._logger = logger,
        self._conversation_handler = conversation_handler

    def add_to_library(self, update: Update, context: CallbackContext):
        query = update.callback_query

        if not context.user_data.get("quality_profile") and query.data.startswith("RadarrQuality"):
            context.user_data["quality_profile"] = query.data.removeprefix("RadarrQuality: ")

        self._conversation_handler.add_to_library(update, context)
