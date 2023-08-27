from abc import ABC, abstractmethod

from src.infrastructure.media_server import MediaServer


class IMediaServerFactory(ABC):
    @abstractmethod
    def get_media_server(self, library_type: str) -> MediaServer:
        """Returns Media Server"""
