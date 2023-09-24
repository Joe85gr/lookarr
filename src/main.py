#!/usr/bin/env python
import os
from os import path, makedirs
from kink import inject
from telegram import Update
from datetime import timedelta

from src.constants import MEDIA_SELECTED, QUALITY_SELECTED, SEASON_SELECTION, \
    DELETE_CONFIRMED, SEARCH_STARTED, MEDIA_TYPE_SELECTED
from src.dependencies.services import configure_services

from src.domain.handlers.interfaces.iauthentication_handler import IAuthHandler
from src.domain.handlers.interfaces.ihandler import IHandler

from telegram.ext import CommandHandler, CallbackQueryHandler, Application, ConversationHandler
from src.domain.config.app_config import Config
from src.domain.handlers.interfaces.ihelp_handler import IHelpHandler
from src.domain.handlers.interfaces.imovie_handler import IMovieHandler
from src.domain.handlers.interfaces.istop_handler import IStopHandler
from src.domain.handlers.interfaces.iseries_handler import ISeriesHandler
from src.domain.validators.env_validator import EnvValidator
from src.infrastructure.interfaces.IDatabase import IDatabase


@inject
def initialise(db: IDatabase, config: Config) -> None:
    if not path.exists("logs"):
        makedirs("logs")

    db.initialise()
    env = EnvValidator()
    env.verify_required_env_variables_exist(config.radarr.enabled, config.sonarr.enabled)
    if not env.is_valid:
        raise ValueError(
            f"Unable to start app as the following required env variables are missing: {', '.join(env.reasons)}")


@inject
def main(
        config: Config,
        authentication_handler: IAuthHandler,
        media_handler: IHandler,
        series_handler: ISeriesHandler,
        movie_handler: IMovieHandler,
        stop_handler: IStopHandler,
        help_handler: IHelpHandler
) -> None:
    application = Application.builder().token(os.getenv("TELEGRAM_BOT_KEY")).build()

    conversation_handler = ConversationHandler(
        per_user=True,
        allow_reentry=True,
        entry_points=[
            CommandHandler(config.lookarr.search_all_command, media_handler.start_search),
            CommandHandler('help', help_handler.help),
            CommandHandler('auth', authentication_handler.authenticate),
            CommandHandler("movie", movie_handler.search_media),
            CommandHandler("series", series_handler.search_media),
        ],
        states={
            SEARCH_STARTED: [
                CallbackQueryHandler(media_handler.search_media, pattern="Sonarr|Radarr")
            ],
            MEDIA_TYPE_SELECTED: [
                CallbackQueryHandler(movie_handler.get_folders, pattern="RadarrGetFolders"),
                CallbackQueryHandler(series_handler.get_folders, pattern="SonarrGetFolders"),
                CallbackQueryHandler(media_handler.change_option, pattern="Next|Previous"),
                CallbackQueryHandler(media_handler.confirm_delete, pattern="ConfirmDelete")
            ],
            MEDIA_SELECTED: [
                CallbackQueryHandler(movie_handler.get_quality_profiles, pattern="RadarrGetQualityProfiles"),
                CallbackQueryHandler(series_handler.get_quality_profiles, pattern="SonarrGetQualityProfiles"),
            ],
            QUALITY_SELECTED: [
                CallbackQueryHandler(movie_handler.add_to_library, pattern="RadarrQuality"),
                CallbackQueryHandler(series_handler.set_quality, pattern="SonarrQuality")
            ],
            SEASON_SELECTION: [
                CallbackQueryHandler(series_handler.add_to_library, pattern="AddSeries"),
                CallbackQueryHandler(series_handler.select_season, pattern="SelectSeason")
            ],
            DELETE_CONFIRMED: [CallbackQueryHandler(media_handler.delete, pattern="Delete")],
        },
        fallbacks=[
            CallbackQueryHandler(stop_handler.stop, pattern="Stop")
        ],
    )

    # Start bot
    application.add_handler(conversation_handler)

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    configure_services()
    initialise()
    main()
