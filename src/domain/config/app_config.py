from pydantic.main import BaseModel
from yaml import safe_load

from src.domain.config.lookarr_config import LookarrConfig
from src.domain.config.radarr_config import RadarrConfig


class Config(BaseModel):
    lookarr: LookarrConfig
    radarr: RadarrConfig


class ConfigLoader:
    @staticmethod
    def load_config(path: str) -> Config:
        with open(f"{path}", "r") as file:
            rawConfig = safe_load(file)

        return Config(**rawConfig)
