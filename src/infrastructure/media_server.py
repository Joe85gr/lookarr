from dataclasses import dataclass
from typing import Type

from src.infrastructure.interfaces.imedia_server_repository import IMediaServerRepository
from src.infrastructure.media_type import TMediaType


@dataclass
class MediaServer:
    media_server: IMediaServerRepository
    data_type: Type[TMediaType]
