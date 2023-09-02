import os
from kink import inject
import json
import requests
from src.domain.config.app_config import Config
from src.infrastructure.api_query import ApiConfig
from src.infrastructure.interfaces.imedia_server_repository import IMediaServerRepository
from src.infrastructure.media_server_repository import IMediaServerRepositoryBase
from src.infrastructure.radarr.movie import Movie
from urllib.parse import quote
from src.logger import ILogger


@inject
class Radarr(IMediaServerRepository):
    def __init__(self, logger: ILogger, config: Config, client: requests, media_server: IMediaServerRepositoryBase):
        self._config = config.radarr
        self._logger = logger
        self._requests = client
        self._media_server = media_server
        self._api_key_identifier = "RADARR_API_KEY"

    @property
    def defaults(self) -> dict:
        return self._config.defaults

    @property
    def _api_query(self):
        return ApiConfig(url=self._config.url, port=self._config.port)

    @property
    def media_type(self):
        return Movie

    def search(self, title: str = None, tmdbid: int = None) -> dict:
        parameters = {"term": f"tmdb:{tmdbid}" if tmdbid else quote(title)}
        url = self._generate_api_query("movie/lookup", parameters)

        return self._media_server.search(url, self._api_key_identifier)

    def get_my_library(self) -> list[Movie]:
        url = self._generate_api_query("movie/lookup")
        return self._media_server.get_my_library(url, self._api_key_identifier, Movie)

    def add_to_library(self, user_data: dict) -> bool:
        parameters = {"tmdbId": str(user_data['id'])}

        req = self._requests.get(
            self._generate_api_query("movie/lookup/tmdb", parameters),
            headers={'X-Api-Key': str(os.environ.get("RADARR_API_KEY"))}
        )

        parsed_json = json.loads(req.text)

        data = self._build_data(parsed_json, user_data['path'], user_data['quality_profile'])

        return self._media_server.add_to_library(data, self._generate_api_query("movie"), self._api_key_identifier,)

    def remove_from_library(self, media_id: int) -> bool:
        query = f'{self._generate_api_query(f"movie")}/{media_id}'
        return self._media_server.remove_from_library(query, self._api_key_identifier)

    def get_root_folders(self):
        query = self._generate_api_query("Rootfolder")
        return self._media_server.get_root_folders(query, self._api_key_identifier)

    def get_quality_profiles(self):
        query = self._generate_api_query("qualityProfile")
        return self._media_server.get_quality_profiles(query, self._api_key_identifier)

    def _generate_api_query(self, endpoint: str, parameters: dict = None):
        return self._media_server.generate_api_query(self._api_query, endpoint, parameters)

    @staticmethod
    def _build_data(json_data, path, quality_profile_id):
        built_data = {
            "qualityProfileId": int(quality_profile_id),
            "rootFolderPath": path,
            "addOptions": {"searchForMovie": True},
        }

        required_fields = ["tmdbId", "year", "title", "titleSlug", "images"]

        for key in required_fields:
            built_data[key] = json_data[key]
        return built_data
