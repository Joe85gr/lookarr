from kink import di
from typing import List
import requests
from src.constants import CONFIG_FULL_PATH
from src.domain.checkers.defaults_checker import DefaultValuesChecker
from src.domain.checkers.idefaults_checker import IDefaultValuesChecker
from src.domain.config.app_config import Config
from src.domain.config.config_loader import ConfigLoader
from src.domain.handlers.help_handler import HelpHandler
from src.domain.handlers.interfaces.ihelp_handler import IHelpHandler
from src.domain.handlers.interfaces.imovie_handler import IMovieHandler
from src.domain.handlers.movie_handler import MovieHandler
from src.domain.handlers.series_handler import SeriesHandler
from src.domain.handlers.interfaces.iseries_handler import ISeriesHandler
from src.infrastructure.interfaces.IDatabase import IDatabase
from src.infrastructure.db.sqlite import Database
from src.infrastructure.interfaces.imedia_server_factory import IMediaServerFactory
from src.infrastructure.interfaces.imedia_server_repository import IMediaServerRepository
from src.infrastructure.media_server_factory import MediaServerFactory
from src.domain.auth.authentication import Auth
from src.domain.auth.interfaces.iauthentication import IAuth
from src.infrastructure.media_server_repository import IMediaServerRepositoryBase, MediaServer
from src.infrastructure.radarr.radarr import Radarr
from src.domain.handlers.authentication_handler import AuthHandler
from src.domain.handlers.interfaces.iauthentication_handler import IAuthHandler
from src.domain.handlers.handler import Handler
from src.domain.handlers.interfaces.ihandler import IHandler
from src.domain.handlers.interfaces.istop_handler import IStopHandler
from src.domain.handlers.stop_handler import StopHandler
from src.infrastructure.sonarr.sonarr import Sonarr


def configure_services() -> None:
    di[Config] = ConfigLoader().load_config(CONFIG_FULL_PATH)
    di[IDatabase] = Database()
    di[IAuth] = Auth()
    di["client"] = requests

    di[IDefaultValuesChecker] = DefaultValuesChecker()

    di[IMediaServerRepositoryBase] = MediaServer()

    di[List[IMediaServerRepository]] = [
        Radarr(),
        Sonarr()
    ]

    di[IMediaServerFactory] = MediaServerFactory()
    di[IAuthHandler] = AuthHandler()
    di[IHandler] = Handler()
    di[IStopHandler] = StopHandler()
    di[IHelpHandler] = HelpHandler()
    di[IMovieHandler] = MovieHandler()
    di[ISeriesHandler] = SeriesHandler()
