import os

from dacite import from_dict
from kink import inject
import requests
import json


from src.domain.config.app_config import Config
from src.infrastructure.media_server import IMediaServerRepository
from src.infrastructure.radarr.movie import Movie
from urllib.parse import quote
from src.logger import ILogger


@inject
class Radarr(IMediaServerRepository):
    def __init__(self, logger: ILogger, config: Config):
        self.config = config.radarr
        self._logger = logger

    @property
    def media_type_name(self) -> str:
        return "Movie"

    @property
    def media_type(self):
        return Movie

    def search(self, title: str = None, tmdbid: int = None) -> dict:

        parameters = {"term": f"tmdb:{tmdbid}" if tmdbid else quote(title)}
        url = self._generate_api_query("movie/lookup", parameters)
        response = requests.get(url, headers={'X-Api-Key': str(os.environ.get("RADARR_API_KEY"))})

        if response.status_code == 200:
            parsed_json = json.loads(response.text)
            return parsed_json
        else:
            self._logger.error(f"Radarr error while searching {title} status code: {response.status_code}")
            return {}

    def get_my_library(self) -> list[Movie]:
        url = self._generate_api_query("movie/lookup")
        response = requests.get(url, headers={'X-Api-Key': str(os.environ.get("RADARR_API_KEY"))})

        if response.status_code == 200:
            parsed_json = json.loads(response.text)
            movies = [from_dict(data_class=Movie, data=entry) for entry in parsed_json]
            return movies
        else:
            return []

    def _generate_api_query(self, endpoint: str, parameters: dict = None):
        url = (
                f"http://{self.config.url}:{self.config.port}/" +
                "api/v3/" + str(endpoint)
        )

        if parameters:
            url += "?"
            for key, value in parameters.items():
                url += "&" + key + "=" + value
        return url.replace(" ", "%20").replace("?&", "?")

    def add_to_library(self, id: int, path: str, qualityProfileId) -> bool:
        parameters = {"tmdbId": str(id)}
        req = requests.get(
            self._generate_api_query("movie/lookup/tmdb", parameters),
            headers={'X-Api-Key': str(os.environ.get("RADARR_API_KEY"))}
        )
        parsed_json = json.loads(req.text)
        data = json.dumps(self.build_data(parsed_json, path, qualityProfileId))
        add = requests.post(self._generate_api_query("movie"), data=data,
                            headers={'Content-Type': 'application/json',
                                     'X-Api-Key': str(os.environ.get("RADARR_API_KEY"))})
        if add.status_code == 201:
            return True
        else:
            self._logger.error(f"Radarr error while adding {id} status code: {add.status_code}, error: {add.text}")
            return False

    def remove_from_library(self, id: int) -> bool:
        query = f'{self._generate_api_query(f"movie")}/{id}'
        req = requests.delete(
            query,
            headers={'X-Api-Key': str(os.environ.get("RADARR_API_KEY"))})
        if req.status_code == 200:
            return True
        else:
            self._logger.error(f"Radarr error while removing {id} status code: {req.status_code}, error: {req.text}")
            return False

    def get_root_folders(self):
        req = requests.get(self._generate_api_query("Rootfolder"),
                           headers={'X-Api-Key': str(os.environ.get("RADARR_API_KEY"))})

        if req.status_code == 200:
            parsed_json = json.loads(req.text)
            return parsed_json

        return {}

    def get_quality_profiles(self):
        req = requests.get(self._generate_api_query("qualityProfile"),
                           headers={'X-Api-Key': str(os.environ.get("RADARR_API_KEY"))})
        parsed_json = json.loads(req.text)
        return parsed_json

    @staticmethod
    def build_data(json_data, path, quality_profile_id):
        built_data = {
            "qualityProfileId": int(quality_profile_id),
            "rootFolderPath": path,
            "addOptions": {"searchForMovie": True},
        }

        addMovieNeededFields = ["tmdbId", "year", "title", "titleSlug", "images"]

        for key in addMovieNeededFields:
            built_data[key] = json_data[key]
        return built_data
