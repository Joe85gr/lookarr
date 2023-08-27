import os
import json
from unittest.mock import Mock, MagicMock
import pytest
from kink import di

from src.domain.config.app_config import Config
from src.domain.config.radarr_config import RadarrConfig
from src.logger import ILogger

mock_config = MagicMock()
di[Config] = mock_config
di[ILogger] = Mock()

from src.infrastructure.radarr.radarr import Radarr
from tests.data.radarr import VALID_RESPONSE


class Test_Radarr:
    @pytest.fixture(autouse=True)
    def before_each(self):
        self._url = "1.1.1.1"
        self._port = "7878"

    def test_search_returns_valid_response(self, requests_mock):
        # Arrange
        os.environ["RADARR_API_KEY"] = "some-api-key"
        expectedResult = VALID_RESPONSE

        mock_config.radarr = RadarrConfig(url=self._url, port=self._port, enabled=True)

        requests_mock.get(f'http://{self._url}:{self._port}/api/v3/movie/lookup?term=Harry%20Potter',
                          text=json.dumps(VALID_RESPONSE), status_code=200)

        config = RadarrConfig(url=self._url, port=self._port, enabled=True)
        sut = Radarr(config)
        title = "Harry Potter"

        # Act
        result = sut.search(title)

        # Assess
        assert result == expectedResult

    def test_search_returns_500(self, requests_mock):
        # Arrange
        os.environ["RADARR_API_KEY"] = "some-api-key"

        requests_mock.get(f'http://{self._url}:{self._port}/api/v3/movie/lookup?term=Harry%20Potter',
                          text="{}",
                          status_code=500)

        mock_config.radarr = RadarrConfig(url=self._url, port=self._port, enabled=True)

        sut = Radarr()
        title = "Harry Potter"

        # Act
        result = sut.search(title)

        # Assess
        assert result == {}
