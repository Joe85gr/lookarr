from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from src.constants import DEFAULT_IMAGE


@dataclass
class Series:
    title: str
    added: str
    year: Optional[int]
    tvdbId: Optional[int]
    certification: Optional[str]
    genres: Optional[list[str]]
    overview: Optional[str]
    certification: Optional[str]
    youTubeTrailerId: Optional[str]
    status: Optional[str]
    youtubeTrailerUrl: str = None
    hasFile: bool = False
    remotePoster: Optional[str] = DEFAULT_IMAGE
    defaultPoster: str = DEFAULT_IMAGE

    @property
    def id(self) -> int:
        return self.tvdbId

    @property
    def is_in_library(self):
        return self.added != '0001-01-01T00:00:00Z'

    def __post_init__(self):
        if self.youTubeTrailerId:
            self.youtubeTrailerUrl = f"https://www.youtube.com/watch?v={self.youTubeTrailerId}"

