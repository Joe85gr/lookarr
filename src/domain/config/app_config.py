from pydantic.main import BaseModel

from src.domain.config.lookarr_config import LookarrConfig
from src.domain.config.media_server_config import MediaServerConfig


class Config(BaseModel):
    lookarr: LookarrConfig
    radarr: MediaServerConfig
    sonarr: MediaServerConfig
    active_media_servers: int = 0
    default_media_server: str = None

    def __init__(self, **data):
        super().__init__(**data)
        self.__post_init__()

    def __post_init__(self):
        for attr, value in self.__dict__.items():
            if type(value) == MediaServerConfig and value.enabled:
                self.active_media_servers += 1
                self.default_media_server = attr.title()
