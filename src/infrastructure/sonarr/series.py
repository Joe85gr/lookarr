from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Series:
    title: str
    added: str
    year: Optional[int]
    tmdbId: Optional[int]
    certification: Optional[str]
    genres: Optional[list[str]]
    overview: Optional[str]
    certification: Optional[str]
    youTubeTrailerId: Optional[str]
    status: Optional[str]
    youtubeTrailerUrl: str = None
    hasFile: bool = False
    remotePoster: Optional[str] = "https://artworks.thetvdb.com/banners/images/missing/movie.jpg"

    @property
    def is_in_library(self):
        return datetime.strptime(self.added, '%Y-%m-%dT%H:%M:%SZ').year != 1

    def __post_init__(self):
        if self.youTubeTrailerId:
            self.youtubeTrailerUrl = f"https://www.youtube.com/watch?v={self.youTubeTrailerId}"
