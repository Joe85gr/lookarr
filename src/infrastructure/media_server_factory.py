from typing import List

from kink import inject

from src.infrastructure.interfaces.imedia_server_factory import IMediaServerFactory
from src.infrastructure.media_server import MediaServer
from src.infrastructure.interfaces.imedia_server_repository import IMediaServerRepository


@inject
class MediaServerFactory(IMediaServerFactory):
    def __init__(self, media_servers: List[IMediaServerRepository]):
        self._systems = {}

        for media_server in media_servers:
            self._systems[media_server.media_type_name] = MediaServer(media_server, media_server.media_type)

    def get_media_server(self, library_type: str) -> MediaServer:
        return self._systems[library_type]
