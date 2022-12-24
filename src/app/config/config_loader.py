from abc import ABC, abstractmethod

from yaml import safe_load

from src.app.config.all_config import Config
from src.constants import CONFIG_FULL_PATH


class IConfigLoader(ABC):
    @staticmethod
    @abstractmethod
    def set_config() -> str:
        pass


class ConfigLoader(IConfigLoader):
    @staticmethod
    def set_config() -> Config:
        with open(f"{CONFIG_FULL_PATH}", "r") as file:
            rawConfig = safe_load(file)

        return Config(**rawConfig)

