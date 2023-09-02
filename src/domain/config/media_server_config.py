from dataclasses import dataclass
from typing import Optional, Any


@dataclass
class MediaServerConfig:
    url: Optional[str]
    port: Optional[str]
    defaults: Optional[dict[str, Any]]
    enabled: Optional[bool] = False
