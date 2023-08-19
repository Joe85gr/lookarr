from abc import abstractmethod, ABC

from src.domain.config.app_config import config
from src.infrastructure.media_server import MediaServer
from src.infrastructure.radarr.movie import Movie
from src.infrastructure.radarr.radarr import Radarr


class IMediaServerFactory(ABC):
    @abstractmethod
    def getMediaServer(self, library_type: str) -> MediaServer:
        """Returns Media Server"""


class MediaServerFactory(IMediaServerFactory):
    def __init__(self):
        self.__systems = {
            "Movie": MediaServer(Radarr(config.radarr), Movie)
        }

    def getMediaServer(self, library_type: str) -> MediaServer:
        return self.__systems[library_type]
