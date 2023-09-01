from dataclasses import dataclass
from typing import Optional


@dataclass
class MediaServerConfig:
    url: Optional[str]
    port: Optional[str]
    enabled: Optional[bool] = False
    default_quality_profile: Optional[str] = None
