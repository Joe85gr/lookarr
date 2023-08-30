from pydantic.main import BaseModel

from src.domain.config.lookarr_config import LookarrConfig
from src.domain.config.media_server_config import MediaServerConfig


class Config(BaseModel):
    lookarr: LookarrConfig
    radarr: MediaServerConfig
    sonarr: MediaServerConfig
