import json
import os

from src.infrastructure.radarr import Radarr
from src.app.config.radarr_config import RadarrConfig

url = "1.1.1.1"
port = "7878"


class Test_Radarr:
    def test_search_returns_valid_response(self, requests_mock):
        # Arrange
        os.environ["RADARR_API_KEY"] = "some-api-key"

        with open("tests/data/radarr_valid_response.json", "r") as file:
            rawData = file.read()
            expectedResult = json.loads(rawData)

        requests_mock.get(f'http://{url}:{port}/api/v3/movie/lookup?term=Harry%20Potter',
                          text=rawData, status_code=200)

        config = RadarrConfig(url=url, port=port, enabled=True)
        sut = Radarr(config)
        title = "Harry Potter"

        # Act
        result = sut.search(title)

        # Assess
        assert result == expectedResult

    def test_search_returns_500(self, requests_mock):
        # Arrange
        os.environ["RADARR_API_KEY"] = "some-api-key"

        requests_mock.get(f'http://{url}:{port}/api/v3/movie/lookup?term=Harry%20Potter',
                          text="{}",
                          status_code=500)

        config = RadarrConfig(url=url, port=port, enabled=True)
        sut = Radarr(config)
        title = "Harry Potter"

        # Act
        result = sut.search(title)

        # Assess
        assert result == {}
