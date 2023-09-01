import os
from kink import inject
import json
import requests
from src.domain.config.app_config import Config
from src.domain.config.media_server_config import MediaServerConfig
from src.infrastructure.api_query import ApiConfig
from src.infrastructure.interfaces.imedia_server_repository import IMediaServerRepository
from urllib.parse import quote

from src.infrastructure.media_server_repository import IMediaServerRepositoryBase
from src.infrastructure.sonarr.series import Series
from src.logger import ILogger


@inject
class Sonarr(IMediaServerRepository):
    def __init__(self, logger: ILogger, config: Config, client: requests, media_server: IMediaServerRepositoryBase):
        self._config: MediaServerConfig = config.sonarr
        self._logger = logger
        self._requests = client
        self._media_server = media_server
        self._api_key_identifier = "SONARR_API_KEY"

    @property
    def default_quality_profile(self):
        return self._config.default_quality_profile

    @property
    def _api_query(self):
        return ApiConfig(url=self._config.url, port=self._config.port)

    @property
    def media_type(self):
        return Series

    @staticmethod
    def set_search_params(user_data: dict) -> dict:
        parameters = {"term": quote(user_data['title'])}
        return parameters

    def search(self, title: str = None, tmdbid: int = None) -> dict:
        parameters = {"term": quote(title)}
        query = self.generate_api_query("series/lookup", parameters)

        return self._media_server.search(query,  self._api_key_identifier)

    def get_my_library(self) -> list[Series]:
        query = self.generate_api_query("series/lookup")
        return self._media_server.get_my_library(query,  self._api_key_identifier, Series)

    def add_to_library(self, user_data: dict) -> bool:
        language_id = self._get_language_profile_id("English")

        seasons = []

        for season in user_data['seasons']:
            if season["selected"]:
                seasons.append({"seasonNumber": season["seasonNumber"], "monitored": True})

        parameters = {
            "term": f"tvdb:{user_data['id']}",
            "languageProfileId": str(language_id),
        }

        req = self._requests.get(
            self.generate_api_query("series/lookup", parameters),
            headers={'X-Api-Key': str(os.environ.get("SONARR_API_KEY"))}
        )

        parsed_json = json.loads(req.text)[0]

        data = self._build_data(parsed_json, user_data['path'], user_data['quality_profile'], language_id, seasons)

        return self._media_server.add_to_library(data, self.generate_api_query("series"), self._api_key_identifier)

    def remove_from_library(self, media_id: int) -> bool:
        query = f'{self.generate_api_query(f"series")}/{media_id}'
        return self._media_server.remove_from_library(query, self._api_key_identifier)

    def get_root_folders(self):
        query = self.generate_api_query("Rootfolder")
        return self._media_server.get_root_folders(query, self._api_key_identifier)

    def get_quality_profiles(self):
        query = self.generate_api_query("qualityProfile")
        return self._media_server.get_quality_profiles(query, self._api_key_identifier)

    def generate_api_query(self, endpoint: str, parameters: dict = None):
        return self._media_server.generate_api_query(self._api_query, endpoint, parameters)

    def _get_language_profile_id(self, language):
        req = requests.get(self.generate_api_query("languageProfile"),
                           headers={'X-Api-Key': str(os.environ.get("SONARR_API_KEY"))})
        parsed_json = req.json()
        language_id = next((lang["id"] for lang in parsed_json if lang["name"] == language), parsed_json[0]["id"])

        return language_id

    @staticmethod
    def _build_data(json_data, path, quality_profile_id, language_id, seasons):
        built_data = {
            "qualityProfileId": int(quality_profile_id),
            "rootFolderPath": path,
            "addOptions": {"searchForMovie": True},
            "languageProfileId": language_id,
            "seasons": seasons,
        }

        required_fields = ["tvdbId", "tvRageId", "title", "titleSlug", "images"]

        for key in required_fields:
            built_data[key] = json_data[key]
        return built_data
