from dataclasses import dataclass
from typing import Optional


@dataclass
class Rating:
    votes: Optional[int]
    value: Optional[float]
    type: Optional[str]


@dataclass
class Ratings:
    imdb: Optional[Rating]
    tmdb: Optional[Rating]