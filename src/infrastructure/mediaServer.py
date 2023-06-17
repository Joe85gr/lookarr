from abc import ABC, abstractmethod
from typing import TypeVar, Type

from pydantic import BaseModel

T = TypeVar('T')


class IMediaServer(ABC):
    @abstractmethod
    def search(self, title: str = None, id: int = None) -> dict:
        """Returns Search Results"""

    @abstractmethod
    def getMyLibrary(self) -> list:
        """Returns Library Results"""

    @abstractmethod
    def addToLibrary(self, id: int, path: str, qualityProfileId):
        """Adds Entry to Library"""

    @abstractmethod
    def getRootFolders(self):
        """Returns List Folders"""

    @abstractmethod
    def getQualityProfiles(self):
        """Returns List Quality Profiles Set on the Library"""


class System:
    def __init__(self, media_server: IMediaServer, data_type: Type[T]):
        self.__mediaServer = media_server
        self.__dataType = data_type

    @property
    def mediaServer(self) -> IMediaServer:
        return self.__mediaServer

    @property
    def dataType(self) -> Type[T]:
        return self.__dataType
