from pydantic.main import BaseModel
from yaml import safe_load

from src.domain.config.lookarr_config import LookarrConfig
from src.domain.config.radarr_config import RadarrConfig


class Config(BaseModel):
    lookarr: LookarrConfig
    radarr: RadarrConfig


class ConfigLoader(object):
    _instance = None
    _config = None

    def __new__(cls, path: str = None):
        if cls._instance is None:
            if path is None:
                raise ValueError("Path cannot be None")
            cls._instance = super(ConfigLoader, cls).__new__(cls)
            cls._config = cls._load_config(path)
        return cls._config

    @staticmethod
    def _load_config(path: str) -> Config:
        with open(f"{path}", "r") as file:
            rawConfig = safe_load(file)

        return Config(**rawConfig)
