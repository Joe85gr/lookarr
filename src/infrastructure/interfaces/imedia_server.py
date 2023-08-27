from abc import abstractmethod
from typing import Protocol


class IMediaServerRepository(Protocol):
    @property
    @abstractmethod
    def media_type_name(self) -> str:
        """Returns type name of Media Server"""

    @property
    @abstractmethod
    def media_type(self):
        """Returns type of Media Server"""

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
