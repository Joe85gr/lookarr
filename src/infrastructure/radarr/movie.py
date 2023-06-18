from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from src.constants import YOUTUBE_BASE_URL, DEFAULT_IMAGE
from src.infrastructure.ratings import Ratings


@dataclass
class Image:
    covertType: Optional[str]
    url: Optional[str]
    remoteUrl: Optional[str]


@dataclass
class Movie:
    title: str
    added: str
    titleSlug: str
    images: Optional[list[Image]]
    year: Optional[int]
    tmdbId: Optional[int]
    certification: Optional[str]
    genres: Optional[list[str]]
    overview: Optional[str]
    ratings: Optional[Ratings]
    hasFile: bool = False
    youTubeTrailerId: Optional[str] = None
    remotePoster: Optional[str] = DEFAULT_IMAGE
    defaultPoster: str = DEFAULT_IMAGE

    @property
    def is_in_library(self):
        return datetime.strptime(self.added, '%Y-%m-%dT%H:%M:%SZ').year != 1

    @property
    def id(self) -> int:
        return self.tmdbId

    @property
    def youtubeTrailerUrl(self):
        if self.youTubeTrailerId:
            return f"{YOUTUBE_BASE_URL}{self.youTubeTrailerId}"
        else:
            return None


