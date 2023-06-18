from typing import TypeVar

from src.infrastructure.radarr.movie import Movie
from src.infrastructure.sonarr.series import Series

TMediaType = TypeVar('TMediaType', Movie, Series)
