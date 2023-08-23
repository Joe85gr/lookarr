from abc import abstractmethod, ABC

from src.domain.config.app_config import ConfigLoader
from src.infrastructure.media_server import MediaServer
from src.infrastructure.radarr.movie import Movie
from src.infrastructure.radarr.radarr import Radarr


class IMediaServerFactory(ABC):
    @abstractmethod
    def get_media_server(self, library_type: str) -> MediaServer:
        """Returns Media Server"""


class MediaServerFactory(IMediaServerFactory):
    def __init__(self):
        config = ConfigLoader().radarr
        self._systems = {
            "Movie": MediaServer(Radarr(config), Movie)
        }

    def get_media_server(self, library_type: str) -> MediaServer:
        return self._systems[library_type]
