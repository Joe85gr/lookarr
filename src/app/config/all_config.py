from pydantic import BaseModel

from src.app.config.lookarr_config import LookarrConfig
from src.app.config.radarr_config import RadarrConfig


class Config(BaseModel):
    lookarr: LookarrConfig
    radarr: RadarrConfig
