from telegram import Update
from telegram.ext import CallbackContext
from kink import inject

from src.domain.checkers.authentication_checker import check_user_is_authenticated
from src.domain.checkers.conversation_checker import check_conversation
from src.domain.checkers.idefaults_checker import IDefaultValuesChecker
from src.domain.handlers.interfaces.imedia_handler import IMediaHandler
from src.domain.handlers.interfaces.imovie_handler import IMovieHandler
from src.domain.handlers.messages_handler import MessagesHandler
from src.infrastructure.interfaces.imedia_server_factory import IMediaServerFactory
from src.logger import ILogger


@inject
class MovieHandler(IMovieHandler):
    def __init__(self,
                 media_server_factory: IMediaServerFactory,
                 logger: ILogger,
                 conversation_handler: IMediaHandler,
                 defaults: IDefaultValuesChecker):
        self._media_server_factory = media_server_factory
        self._logger = logger
        self._conversation_handler = conversation_handler
        self._defaults = defaults

    @check_user_is_authenticated
    @check_conversation(["update_msg", "type"])
    def get_quality_profiles(self, update: Update, context: CallbackContext):
        MessagesHandler.delete_current_and_add_new(context, update, ".. 👀")

        query = update.callback_query

        context.user_data["path"] = query.data.removeprefix("RadarrGetQualityProfiles: ")

        media_server = self._media_server_factory.get_media_server(context.user_data["type"])

        valid_values = media_server.media_server.get_quality_profiles()
        has_default_profile = self._defaults.check_defaults("quality_profile", valid_values, media_server, context)

        if has_default_profile:
            self.add_to_library(update, context)
        else:
            self._conversation_handler.get_quality_profiles(update, context)

    def add_to_library(self, update: Update, context: CallbackContext):
        query = update.callback_query

        if not context.user_data.get("quality_profile") and query.data.startswith("RadarrQuality"):
            context.user_data["quality_profile"] = query.data.removeprefix("RadarrQuality: ")

        self._conversation_handler.add_to_library(update, context)
