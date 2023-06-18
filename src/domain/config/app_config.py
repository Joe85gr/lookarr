from abc import ABC, abstractmethod

from pydantic.main import BaseModel
from yaml import safe_load
from src.domain.config.lookarr_config import LookarrConfig
from src.domain.config.radarr_config import RadarrConfig
from src.constants import CONFIG_FULL_PATH


class Config(BaseModel):
    lookarr: LookarrConfig
    radarr: RadarrConfig


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
