from yaml import safe_load
from kink import inject

from src import Logger
from src.domain.config.app_config import Config


@inject
class ConfigLoader:
    def __init__(self, logger: Logger):
        self._logger = logger

    def load_config(self, config_full_path: str) -> Config:
        try:
            with open(f"{config_full_path}", "r") as file:
                rawConfig = safe_load(file)

            return Config(**rawConfig)
        except FileNotFoundError:
            import shutil
            from os import path
            from pathlib import Path

            self._logger.error(f"Config file not found at {config_full_path}. "
                               f"Creating default config..")

            config_path = Path(config_full_path).parent
            sample_config_path = Path(__file__).parents[2]
            shutil.copyfile(f"{sample_config_path}/config-sample.yml", config_full_path)

            return self.load_config(f"{config_path}/config.yml")
