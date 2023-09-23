import os
from abc import ABC, abstractmethod
from typing import Type

from dacite import from_dict
from kink import inject
import json
import requests

from src.infrastructure.api_query import ApiConfig
from src.infrastructure.media_type import TMediaType
from src.logger import Logger


class IMediaServerRepositoryBase(ABC):
    @abstractmethod
    def search(self, query: str, api_key_env_identifier: str) -> dict:
        """Search media"""

    @abstractmethod
    def get_my_library(self, query: str, api_key_env_identifier: str, media_type) -> list:
        """Get library"""

    @abstractmethod
    def add_to_library(self, parameters: dict, query: str, api_key_env_identifier: str) -> bool:
        """Add media to library"""

    @abstractmethod
    def remove_from_library(self, query: str, api_key_env_identifier: str) -> bool:
        """Remove media from library"""

    @abstractmethod
    def get_root_folders(self, query: str, api_key_env_identifier: str):
        """Get root folders"""

    @abstractmethod
    def get_quality_profiles(self, query: str, api_key_env_identifier: str):
        """Get quality profiles"""

    @staticmethod
    @abstractmethod
    def generate_api_query(api_query: ApiConfig, endpoint: str, parameters: dict = None):
        """Generate api query"""

    @abstractmethod
    def set_api_query(self, api_query: ApiConfig):
        """Set api query"""


@inject
class MediaServer(IMediaServerRepositoryBase):
    def __init__(self, logger: Logger, client: requests):
        self._logger = logger
        self._requests = client

        self._api_query = None

    def set_api_query(self, api_query: ApiConfig):
        self._api_query = api_query

    def search(self, query: str, api_key_env_identifier: str) -> dict:
        response = self._requests.get(query, headers={'X-Api-Key': str(os.environ.get(api_key_env_identifier))})

        if response.status_code == 200:
            return response.json()
        else:
            self._logger.error(f"Error while searching media status code: {response.status_code}")
            return {}

    def get_my_library(self, query: str, api_key_env_identifier: str, media_type: Type[TMediaType]) -> list:
        response = self._requests.get(query, headers={'X-Api-Key': str(os.environ.get(api_key_env_identifier))})

        if response.status_code == 200:
            parsed_json = json.loads(response.text)
            library = [from_dict(data_class=media_type, data=entry) for entry in parsed_json]
            return library
        else:
            return []

    def add_to_library(self, parameters: dict, query: str, api_key_env_identifier: str) -> bool:
        data = json.dumps(parameters)

        response = self._requests.post(query,
                                       data=data,
                                       headers={'Content-Type': 'application/json',
                                                'X-Api-Key': str(os.environ.get(api_key_env_identifier))})

        if response.status_code == 201:
            return True
        else:
            self._logger.error(f"Error while adding media {parameters} "
                               f"status code: {response.status_code}, error: {response.text}")
            return False

    def remove_from_library(self, query: str, api_key_env_identifier: str) -> bool:
        response = self._requests.delete(
            query,
            headers={'X-Api-Key': str(os.environ.get(api_key_env_identifier))})

        if response.status_code == 200:
            return True
        else:
            self._logger.error(f"Error while removing media status code: {response.status_code}, "
                               f"error: {response.text}")
            return False

    def get_root_folders(self, query: str, api_key_env_identifier: str):
        response = self._requests.get(query, headers={'X-Api-Key': str(os.environ.get(api_key_env_identifier))})

        if response.status_code == 200:
            parsed_json = json.loads(response.text)
            return parsed_json

        return {}

    def get_quality_profiles(self, query: str, api_key_env_identifier: str):
        response = self._requests.get(query, headers={'X-Api-Key': str(os.environ.get(api_key_env_identifier))})
        return response.json()

    @staticmethod
    def generate_api_query(api_query: ApiConfig, endpoint: str, parameters: dict = None):
        url = (
                f"http://{api_query.url}:{api_query.port}/" +
                "api/v3/" + str(endpoint)
        )

        if parameters:
            url += "?"
            for key, value in parameters.items():
                url += "&" + key + "=" + value
        return url.replace(" ", "%20").replace("?&", "?")
