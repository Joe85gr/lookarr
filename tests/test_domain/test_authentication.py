import os
from unittest.mock import patch

from src.domain.auth.authentication import Auth
from src.domain.config.lookarr_config import LookarrConfig


class Test_Auth:
    @patch('src.domain.auth.authentication.db')
    def test_user_is_authenticated(self, mocked_db):
        # Arrange
        mocked_db.user_exists.return_value = True

        sut = Auth()

        # Act
        result = sut.user_is_authenticated(1)

        # Assert
        assert result is True
        mocked_db.user_exists.assert_called_once_with(1)

    @patch('src.domain.auth.authentication.db')
    def test_user_is_not_authenticated(self, mocked_db):
        # Arrange
        mocked_db.user_exists.return_value = False

        sut = Auth()

        # Act
        result = sut.user_is_authenticated(1)

        # Assert
        assert result is False
        mocked_db.user_exists.assert_called_once_with(1)

    def test_user_is_authenticated_strict(self):
        # Arrange
        config = LookarrConfig(
            language="en-us",
            strict_mode=True,
            strict_mode_allowed_ids=[1, 2],
            search_all_command="Search",
        )

        sut = Auth()

        # Act
        result = Auth.user_is_authenticated_strict(1, config)

        # Assert
        assert result is True

    def test_user_is_not_authenticated_strict(self):
        # Arrange
        config = LookarrConfig(
            language="en-us",
            strict_mode=True,
            strict_mode_allowed_ids=[1, 2],
            search_all_command="Search",
        )

        sut = Auth()

        # Act
        result = Auth.user_is_authenticated_strict(3, config)

        # Assert
        assert result is False

    @patch.dict(os.environ, {"LOOKARR_AUTH_PASSWORD": "valid_user"})
    @patch('src.domain.auth.authentication.db')
    def test_authenticate_valid_user(self, mocked_db):
        # Arrange
        sut = Auth()

        # Act
        result = sut.authenticate_user(1, "valid_user")

        # Assert
        assert result is True
        mocked_db.add_user.assert_called_once_with(1)

    @patch.dict(os.environ, {"LOOKARR_AUTH_PASSWORD": "valid_user"})
    @patch('src.domain.auth.authentication.db')
    def test_authenticate_invalid_user(self, mocked_db):
        # Arrange
        sut = Auth()

        # Act
        result = sut.authenticate_user(1, "invalid_user")

        # Assert
        assert result is False
        assert mocked_db.add_user.call_count == 0

    def test_auth_is_singleton(self):
        # Act
        auth1 = Auth()
        auth2 = Auth()

        # Assert
        assert auth1 is auth2
