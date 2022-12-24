from pydantic import BaseModel

from src.app.config.lookarr_config import LookarrConfig


class Config(BaseModel):
    lookarr: LookarrConfig
