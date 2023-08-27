import os
from pathlib import Path
from unittest.mock import Mock, MagicMock
import pytest
from kink import di
from requests import Response

from src.domain.config.app_config import Config, ConfigLoader
from src.domain.config.radarr_config import RadarrConfig
from src.logger import ILogger
from tests.data.radarr import VALID_RESPONSE

path = f"{Path(__file__).parent.parent.parent}/data/config.yml"
mock_config = ConfigLoader.load_config(path)
mock_response = Response()

mock_client = MagicMock()

mock_client.get.return_value = mock_response

di[Config] = mock_config
di[ILogger] = Mock()
di["client"] = mock_client

from src.infrastructure.radarr.radarr import Radarr


class Test_Radarr:
    @pytest.fixture(autouse=True)
    def before_each(self):
        self._url = "1.1.1.1"
        self._port = "7878"

    def test_search_returns_valid_response(self):
        # Arrange
        os.environ["RADARR_API_KEY"] = "some-api-key"
        expectedResult = VALID_RESPONSE

        mock_response.status_code = 200
        mock_response.json = MagicMock(return_value=VALID_RESPONSE)

        mock_config.radarr = RadarrConfig(url=self._url, port=self._port, enabled=True)

        config = RadarrConfig(url=self._url, port=self._port, enabled=True)
        sut = Radarr(config)
        title = "Harry Potter"

        # Act
        result = sut.search(title)

        # Assess
        assert result == expectedResult

    def test_search_returns_500(self):
        # Arrange
        os.environ["RADARR_API_KEY"] = "some-api-key"

        mock_response.status_code = 500

        mock_config.radarr = RadarrConfig(url=self._url, port=self._port, enabled=True)

        sut = Radarr()
        title = "Harry Potter"

        # Act
        result = sut.search(title)

        # Assess
        assert result == {}
