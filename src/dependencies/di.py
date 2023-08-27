from typing import List

from kink import di

from src.constants import CONFIG_FULL_PATH
from src.domain.config.app_config import ConfigLoader, Config
from src.infrastructure.db.IDatabase import IDatabase
from src.infrastructure.db.sqlite import Database
from src.infrastructure.imedia_server_factory import IMediaServerFactory
from src.infrastructure.media_server import IMediaServerRepository
from src.infrastructure.media_server_factory import MediaServerFactory
from src.logger import ILogger, Logger

di[Config] = ConfigLoader(CONFIG_FULL_PATH)
di[IDatabase] = Database()

from src.domain.auth.authentication import Auth
from src.domain.auth.iauthentication import IAuth
from src.infrastructure.radarr.radarr import Radarr

di[IAuth] = Auth()
di[ILogger] = Logger(__name__)
di[List[IMediaServerRepository]] = [Radarr()]
di[IMediaServerFactory] = MediaServerFactory()
