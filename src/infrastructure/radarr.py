import os

from dacite import from_dict
import json

import requests

from src.app.config.radarr_config import RadarrConfig
from src.infrastructure.movie import Movie
from src.logger import Log


class Radarr:
    def __init__(self, config: RadarrConfig):
        self.logger = Log.get_logger("src.infrastructure.radarr.Radarr")
        self.config = config

    def search(self, title) -> list[Movie]:
        parameters = {"term": title}
        url = self.generateApiQuery("movie/lookup", parameters)
        response = requests.get(url)

        if response.status_code == 200:
            parsed_json = json.loads(response.text)
            movies = [from_dict(data_class=Movie, data=entry) for entry in parsed_json]
            return movies
        else:
            return []

    def generateApiQuery(self, endpoint: str, parameters: dict):
        try:
            url = (
                    f"http://{self.config.url}:{self.config.port}/" +
                    "api/v3/" + str(endpoint) +
                    "?apikey=" + str(os.environ.get("RADARR_API_KEY"))
            )

            if parameters:
                for key, value in parameters.items():
                    url += "&" + key + "=" + value
            return url.replace(" ", "%20")
        except Exception as e:
            self.logger.error(f"Generate of APIQUERY failed: {e}.")
