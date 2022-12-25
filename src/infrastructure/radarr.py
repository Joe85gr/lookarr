import os

from dacite import from_dict
import json

import requests

from src.app.config.radarr_config import RadarrConfig
from src.infrastructure.movie import Movie
from src.logger import Log


class Radarr:
    def __init__(self, config: RadarrConfig):
        self.requests = requests
        self.logger = Log.get_logger("src.infrastructure.radarr.Radarr")
        self.config = config

    def search(self, title) -> list[Movie]:
        parameters = {"term": title}
        url = self.generateApiQuery("movie/lookup", parameters)
        req = self.requests.get(url)
        parsed_json = json.loads(req.text)

        if req.status_code == 200 and parsed_json:
            data = [from_dict(data_class=Movie, data=entry) for entry in parsed_json]
            return data
        else:
            return []

    def generateApiQuery(self, endpoint: str, parameters=None):
        if parameters is None:
            parameters = {}
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
