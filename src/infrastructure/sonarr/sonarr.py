import os
from dacite import from_dict
from kink import inject
import json
import requests
from src.domain.config.app_config import Config
from src.infrastructure.interfaces.imedia_server_repository import IMediaServerRepository
from urllib.parse import quote

from src.infrastructure.sonarr.series import Series
from src.logger import ILogger


@inject
class Sonarr(IMediaServerRepository):
    def __init__(self, logger: ILogger, config: Config, client: requests):
        self._config = config.sonarr
        self._logger = logger
        self._requests = client

    @property
    def media_type_name(self) -> str:
        return "Series"

    @property
    def media_type(self):
        return Series

    def search(self, title: str = None, tmdbid: int = None) -> dict:
        parameters = {"term": quote(title)}
        url = self._generate_api_query("series/lookup", parameters)
        response = self._requests.get(url, headers={'X-Api-Key': str(os.environ.get("SONARR_API_KEY"))})
        
        if response.status_code == 200:
            return response.json()
        else:
            self._logger.error(f"Sonarr error while searching {title} status code: {response.status_code}")
            return {}

    def get_my_library(self) -> list[Series]:
        url = self._generate_api_query("series/lookup")
        response = self._requests.get(url, headers={'X-Api-Key': str(os.environ.get("SONARR_API_KEY"))})

        if response.status_code == 200:
            parsed_json = json.loads(response.text)
            series = [from_dict(data_class=Series, data=entry) for entry in parsed_json]
            return series
        else:
            return []

    def add_to_library(self, user_data: dict) -> bool:
        language_id = self._get_language_profile_id("English")

        seasons = []

        if user_data['season'] == "All":
            for season_number in user_data['season_numbers']:
                seasons.append({"seasonNumber": season_number, "monitored": True})
        else:
            seasons.append({"seasonNumber": user_data['season'], "monitored": True})

        parameters = {
            "term": f"tvdb:{user_data['id']}",
            "languageProfileId": str(language_id),
        }

        req = self._requests.get(
            self._generate_api_query("series/lookup", parameters),
            headers={'X-Api-Key': str(os.environ.get("SONARR_API_KEY"))}
        )

        parsed_json = json.loads(req.text)[0]

        data = json.dumps(self._build_data(
            parsed_json, user_data['path'], user_data['quality_profile'], language_id, seasons))
        add = self._requests.post(self._generate_api_query("series"), data=data,
                                  headers={'Content-Type': 'application/json',
                                     'X-Api-Key': str(os.environ.get("SONARR_API_KEY"))})
        if add.status_code == 201:
            return True
        else:
            self._logger.error(f"Sonarr error while adding {user_data['id']} "
                               f"status code: {add.status_code}, error: {add.text}")
            return False

    def remove_from_library(self, id: int) -> bool:
        query = f'{self._generate_api_query(f"series")}/{id}'
        req = self._requests.delete(
            query,
            headers={'X-Api-Key': str(os.environ.get("SONARR_API_KEY"))})
        if req.status_code == 200:
            return True
        else:
            self._logger.error(f"Sonarr error while removing {id} status code: {req.status_code}, error: {req.text}")
            return False

    def get_root_folders(self):
        req = self._requests.get(self._generate_api_query("Rootfolder"),
                                 headers={'X-Api-Key': str(os.environ.get("SONARR_API_KEY"))})

        if req.status_code == 200:
            return req.json()

        return {}

    def get_quality_profiles(self):
        req = self._requests.get(self._generate_api_query("qualityProfile"),
                                 headers={'X-Api-Key': str(os.environ.get("SONARR_API_KEY"))})
        return req.json()

    def _get_language_profile_id(self, language):
        req = requests.get(self._generate_api_query("languageProfile"),
                           headers={'X-Api-Key': str(os.environ.get("SONARR_API_KEY"))})
        parsed_json = req.json()
        language_id = next((lang["id"] for lang in parsed_json if lang["name"] == language), parsed_json[0]["id"])

        return language_id

    def _generate_api_query(self, endpoint: str, parameters: dict = None):
        url = (
                f"http://{self._config.url}:{self._config.port}/" +
                "api/v3/" + str(endpoint)
        )

        if parameters:
            url += "?"
            for key, value in parameters.items():
                url += "&" + key + "=" + value
        return url.replace(" ", "%20").replace("?&", "?")

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
