from src.infrastructure.movie import Movie
from src.infrastructure.ratings import Ratings, Rating


class Test_Movie:
    def test_WhenYoutubeIdIsNotNull_YoutubeUrlIsPopulated(self):
        # Arrange
        expectedYoutubeUrl = "https://www.youtube.com/watch?v=some-youtube-id"

        # Act
        result = Movie(
            title="naruto",
            added="0001-01-01T00:01:00Z",
            titleSlug="some-slug",
            images=[],
            genres=[],
            ratings=Ratings(imdb=Rating(0, 0, ""), tmdb=Rating(0, 0, "")),
            youTubeTrailerId='some-youtube-id',
            year=2005,
            tmdbId=1,
            certification="PG",
            overview="super fancy anime",
        )

        # Assert
        assert result.youtubeTrailerUrl == expectedYoutubeUrl

    def test_WhenYoutubeIdIsNull_YoutubeUrlIsNull(self):
        # Arrange
        expectedYoutubeUrl = None

        # Act
        result = Movie(
            title="naruto",
            added="0001-01-01T00:01:00Z",
            titleSlug="some-slug",
            images=[],
            genres=[],
            ratings=Ratings(imdb=Rating(0, 0, ""), tmdb=Rating(0, 0, "")),
            year=2005,
            tmdbId=1,
            certification="PG",
            overview="super fancy anime",
        )

        # Assert
        assert result.youtubeTrailerUrl == expectedYoutubeUrl
