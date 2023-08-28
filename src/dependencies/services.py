from kink import di
from typing import List
import requests
from src.constants import CONFIG_FULL_PATH
from src.domain.config.app_config import Config
from src.domain.config.config_loader import ConfigLoader
from src.domain.handlers.help_handler import HelpHandler
from src.domain.handlers.interfaces.ihelp_handler import IHelpHandler
from src.infrastructure.interfaces.IDatabase import IDatabase
from src.infrastructure.db.sqlite import Database
from src.infrastructure.interfaces.imedia_server_factory import IMediaServerFactory
from src.infrastructure.interfaces.imedia_server_repository import IMediaServerRepository
from src.infrastructure.media_server_factory import MediaServerFactory
from src.domain.auth.authentication import Auth
from src.domain.auth.interfaces.iauthentication import IAuth
from src.infrastructure.radarr.radarr import Radarr
from src.domain.handlers.authentication_handler import AuthHandler
from src.domain.handlers.interfaces.iauthentication_handler import IAuthHandler
from src.domain.handlers.conversation_handler import SearchHandler
from src.domain.handlers.interfaces.iconversation_handler import ISearchHandler
from src.domain.handlers.interfaces.istop_handler import IStopHandler
from src.domain.handlers.stop_handler import StopHandler


def configure_services() -> None:
    di[Config] = ConfigLoader().load_config(CONFIG_FULL_PATH)
    di[IDatabase] = Database()
    di[IAuth] = Auth()
    di["client"] = requests

    di[List[IMediaServerRepository]] = [
        Radarr()
    ]

    di[IMediaServerFactory] = MediaServerFactory()
    di[IAuthHandler] = AuthHandler()
    di[ISearchHandler] = SearchHandler()
    di[IStopHandler] = StopHandler()
    di[IHelpHandler] = HelpHandler()
