import os

from src.domain.authentication import Auth
from src.app.config.all_config import Config, LookarrConfig
from src.infrastructure.IDatabase import IDatabase


class MockDatabase(IDatabase):
    @staticmethod
    def initialise() -> None:
        pass

    @staticmethod
    def add_user(user: int) -> None:
        pass

    @staticmethod
    def user_exists(user: int):
        pass


class Test_Auth:
    def test_user_is_authenticated_strict_not_enabled(self):
        # Arrange
        sut = Auth(MockDatabase())

        lookarrConfig = LookarrConfig(
            language="en-us",
            strict_mode=False,
            strict_mode_allowed_ids=[],
            search_all_command="Search",
            search_series_command="Series",
            search_movie_command="Movie"
        )

        config = Config(lookarr=lookarrConfig)

        # Act
        result = sut.user_is_authenticated_strict(1, config)

        # Assess
        assert result is True

    def test_user_is_authenticated_strict_enabled_and_user_is_allowed(self):
        # Arrange
        sut = Auth(MockDatabase())
        userId = 123
        lookarrConfig = LookarrConfig(
            language="en-us",
            strict_mode=True,
            strict_mode_allowed_ids=[userId],
            search_all_command="Search",
            search_series_command="Series",
            search_movie_command="Movie"
        )

        config = Config(lookarr=lookarrConfig)

        # Act
        result = sut.user_is_authenticated_strict(userId, config)

        # Assess
        assert result is True

    def test_user_is_authenticated_strict_enabled_and_user_is_not_allowed(self):
        # Arrange
        sut = Auth(MockDatabase())
        userId = 123
        lookarrConfig = LookarrConfig(
            language="en-us",
            strict_mode=True,
            strict_mode_allowed_ids=[999],
            search_all_command="Search",
            search_series_command="Series",
            search_movie_command="Movie"
        )

        config = Config(lookarr=lookarrConfig)

        # Act
        result = sut.user_is_authenticated_strict(userId, config)

        # Assess
        assert result is False

    def test_user_is_authenticated_valid_user(self):
        # Arrange
        userId = 123

        class MockDatabaseValidUser(MockDatabase):
            @staticmethod
            def user_exists(user: int):
                return 1, userId

        sut = Auth(MockDatabaseValidUser())

        # Act
        result = sut.user_is_authenticated(userId)

        # Assess
        assert result is True

    def test_user_is_authenticated_invalid_user(self):
        # Arrange
        userId = 123

        class MockDatabaseInvalidUser(MockDatabase):
            @staticmethod
            def user_exists(user: int):
                return None

        sut = Auth(MockDatabaseInvalidUser())

        # Act
        result = sut.user_is_authenticated(userId)

        # Assess
        assert result is False

    def test_authenticate_user_valid_password(self):
        # Arrange
        userId = 123
        os.environ.clear()
        os.environ["LOOKARR_AUTH_PASSWORD"] = "password"

        sut = Auth(MockDatabase())

        # Act
        result = sut.authenticate_user(userId, "password")

        # Assess
        assert result is True

    def test_authenticate_user_invalid_password(self):
        # Arrange
        userId = 123
        os.environ.clear()
        os.environ["LOOKARR_AUTH_PASSWORD"] = "password"

        sut = Auth(MockDatabase())

        # Act
        result = sut.authenticate_user(userId, "invalid password")

        # Assess
        assert result is False
