import os

from dacite import from_dict
import json

import requests

from src.domain.config.radarr_config import RadarrConfig
from src.infrastructure.media_server import IMediaServerRepository
from src.infrastructure.radarr.movie import Movie
from urllib.parse import quote
from src.logger import Log


class Radarr(IMediaServerRepository):
    def __init__(self, config: RadarrConfig):
        self.logger = Log.get_logger("src.infrastructure.radarr.Radarr")
        self.config = config

    def search(self, title: str = None, tmdbid: int = None) -> dict:

        parameters = {"term": f"tmdb:{tmdbid}" if tmdbid else quote(title)}
        url = self.__generateApiQuery("movie/lookup", parameters)
        response = requests.get(url, headers={'X-Api-Key': str(os.environ.get("RADARR_API_KEY"))})

        if response.status_code == 200:
            parsed_json = json.loads(response.text)
            return parsed_json
        else:
            self.logger.error(f"Radarr error while seaeching {title} status code: {response.status_code}")
            return {}

    def getMyLibrary(self) -> list[Movie]:
        url = self.__generateApiQuery("movie/lookup")
        response = requests.get(url, headers={'X-Api-Key': str(os.environ.get("RADARR_API_KEY"))})

        if response.status_code == 200:
            parsed_json = json.loads(response.text)
            movies = [from_dict(data_class=Movie, data=entry) for entry in parsed_json]
            return movies
        else:
            return []

    def __generateApiQuery(self, endpoint: str, parameters: dict = None):
        url = (
                f"http://{self.config.url}:{self.config.port}/" +
                "api/v3/" + str(endpoint)
        )

        if parameters:
            url += "?"
            for key, value in parameters.items():
                url += "&" + key + "=" + value
        return url.replace(" ", "%20").replace("?&", "?")

    def addToLibrary(self, id: int, path: str, qualityProfileId) -> bool:
        parameters = {"tmdbId": str(id)}
        req = requests.get(
            self.__generateApiQuery("movie/lookup/tmdb", parameters),
            headers={'X-Api-Key': str(os.environ.get("RADARR_API_KEY"))}
        )
        parsed_json = json.loads(req.text)
        data = json.dumps(self.buildData(parsed_json, path, qualityProfileId))
        add = requests.post(self.__generateApiQuery("movie"), data=data,
                            headers={'Content-Type': 'application/json',
                                     'X-Api-Key': str(os.environ.get("RADARR_API_KEY"))})
        if add.status_code == 201:
            return True
        else:
            self.logger.error(f"Radarr error while adding {id} status code: {add.status_code}, error: {add.text}")
            return False

    def removeFromLibrary(self, id: int) -> bool:
        query = f'{self.__generateApiQuery(f"movie")}/{id}'
        req = requests.delete(
            query,
            headers={'X-Api-Key': str(os.environ.get("RADARR_API_KEY"))})
        if req.status_code == 200:
            return True
        else:
            self.logger.error(f"Radarr error while removing {id} status code: {req.status_code}, error: {req.text}")
            return False

    def getRootFolders(self):
        req = requests.get(self.__generateApiQuery("Rootfolder"),
                           headers={'X-Api-Key': str(os.environ.get("RADARR_API_KEY"))})

        if req.status_code == 200:
            parsed_json = json.loads(req.text)
            return parsed_json

        return {}

    def getQualityProfiles(self):
        req = requests.get(self.__generateApiQuery("qualityProfile"),
                           headers={'X-Api-Key': str(os.environ.get("RADARR_API_KEY"))})
        parsed_json = json.loads(req.text)
        return parsed_json

    @staticmethod
    def buildData(json, path, quality_profile_id):
        built_data = {
            "qualityProfileId": int(quality_profile_id),
            "rootFolderPath": path,
            "addOptions": {"searchForMovie": True},
        }

        addMovieNeededFields = ["tmdbId", "year", "title", "titleSlug", "images"]

        for key in addMovieNeededFields:
            built_data[key] = json[key]
        return built_data
