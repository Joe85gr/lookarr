from yaml import safe_load
from kink import inject

from src import ILogger
from src.domain.config.app_config import Config


@inject
class ConfigLoader:
    def __init__(self, logger: ILogger):
        self._logger = logger

    def load_config(self, path: str) -> Config:
        try:
            with open(f"{path}", "r") as file:
                rawConfig = safe_load(file)

            return Config(**rawConfig)
        except FileNotFoundError as e:
            self._logger.error(f"Config file not found at {path}. "
                               f"Please rename the config-sample file to config.yml and set your config.")
            raise e

