from pathlib import Path
from unittest.mock import Mock, MagicMock

from kink import di

from src.domain.config.app_config import Config, ConfigLoader
from src.infrastructure.interfaces.IDatabase import IDatabase
from src.logger import ILogger

di[ILogger] = Mock()
mock_db = MagicMock()
path = f"{Path(__file__).parent}/data/config.yml"
mock_config = ConfigLoader.load_config(path)

di[IDatabase] = mock_db
di[Config] = mock_config
