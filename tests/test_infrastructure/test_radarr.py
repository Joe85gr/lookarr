import os
from src.infrastructure.radarr import Radarr
from src.app.config.radarr_config import RadarrConfig


class Test_Radarr:
    def test_search_returns_valid_response(self):
        # Arrange
        os.environ["RADARR_API_KEY"] = "some-key"
        config = RadarrConfig(url="10.66.66.10", port="7878", enabled=True)
        sut = Radarr(config)
        title = "Harry Potter"

        # Act
        result = sut.search(title)

        # Assess
        assert True is False
