from dataclasses import dataclass
from typing import Optional


@dataclass
class RadarrConfig:
    url: Optional[str]
    port: Optional[str]
    enabled: Optional[bool] = False
