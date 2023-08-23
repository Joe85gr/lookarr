from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Type

from src.infrastructure.media_type import TMediaType


class IMediaServerRepository(ABC):
    @abstractmethod
    def search(self, title: str = None, id: int = None) -> dict:
        """Returns Search Results"""

    @abstractmethod
    def get_my_library(self) -> list:
        """Returns Library Results"""

    @abstractmethod
    def add_to_library(self, id: int, path: str, qualityProfileId) -> bool:
        """Adds Entry to Library"""

    @abstractmethod
    def remove_from_library(self, id: int) -> bool:
        """Removes Entry from Library"""

    @abstractmethod
    def get_root_folders(self):
        """Returns List Folders where Media can  be stored"""

    @abstractmethod
    def get_quality_profiles(self):
        """Returns List Quality Profiles Set on the Library"""


@dataclass
class MediaServer:
    media_server: IMediaServerRepository
    data_type: Type[TMediaType]
