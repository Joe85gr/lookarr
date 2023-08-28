from pydantic.main import BaseModel

from src.domain.config.lookarr_config import LookarrConfig
from src.domain.config.radarr_config import RadarrConfig


class Config(BaseModel):
    lookarr: LookarrConfig
    radarr: RadarrConfig
