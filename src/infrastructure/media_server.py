from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Type

from src.infrastructure.media_type import TMediaType


class IMediaServerRepository(ABC):
    @abstractmethod
    def search(self, title: str = None, id: int = None) -> dict:
        """Returns Search Results"""

    @abstractmethod
    def getMyLibrary(self) -> list:
        """Returns Library Results"""

    @abstractmethod
    def addToLibrary(self, id: int, path: str, qualityProfileId) -> bool:
        """Adds Entry to Library"""

    @abstractmethod
    def getRootFolders(self):
        """Returns List Folders where Media can  be stored"""

    @abstractmethod
    def getQualityProfiles(self):
        """Returns List Quality Profiles Set on the Library"""


@dataclass
class MediaServer:
    media_server: IMediaServerRepository
    data_type: Type[TMediaType]
