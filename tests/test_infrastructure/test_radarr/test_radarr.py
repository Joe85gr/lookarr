import os
import pytest
from unittest.mock import MagicMock
from kink import di
from requests import Response

from src.domain.config.radarr_config import RadarrConfig
from tests.data.radarr import VALID_RESPONSE

mock_response = Response()
mock_client = MagicMock()
mock_client.get.return_value = mock_response

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

        sut = Radarr()
        title = "Harry Potter"

        # Act
        result = sut.search(title)

        # Assess
        assert result == {}
