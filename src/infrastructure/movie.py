from dataclasses import dataclass
from datetime import datetime
from typing import Optional
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
    id: Optional[int] = None
    youtubeTrailerUrl: str = None
    date_added: datetime = None
    hasFile: bool = False
    youTubeTrailerId: Optional[str] = None
    remotePoster: Optional[str] = "https://artworks.thetvdb.com/banners/images/missing/movie.jpg"
    defaultPoster: str = "https://artworks.thetvdb.com/banners/images/missing/movie.jpg"

    def __post_init__(self):
        self.date_added = datetime.strptime(self.added, '%Y-%m-%dT%H:%M:%SZ')
        self.id = self.tmdbId
        if self.youTubeTrailerId:
            self.youtubeTrailerUrl = f"https://www.youtube.com/watch?v={self.youTubeTrailerId}"
