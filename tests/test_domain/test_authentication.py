import os
from unittest.mock import patch, Mock
from kink import di

from src.domain.config.app_config import Config
from src.infrastructure.db.IDatabase import IDatabase
from src.domain.config.lookarr_config import LookarrConfig
import pytest

mock_db = Mock()
mock_config = Mock()

di[IDatabase] = mock_db
di[Config] = mock_config

from src.domain.auth.authentication import Auth


class Test_Auth:
    @pytest.fixture(autouse=True)
    def before_each(self):
        mock_config.lookarr = LookarrConfig(
            language="en-us",
            strict_mode=True,
            strict_mode_allowed_ids=[1, 2],
            search_all_command="Search",
        )

    def test_user_is_authenticated(self):
        # Arrange
        mock_db.user_exists.return_value = True

        sut = Auth()

        # Act
        result = sut.user_is_authenticated(1)

        # Assert
        assert result is True
        mock_db.user_exists.assert_called_once_with(1)

    def test_user_is_not_authenticated(self):
        # Arrange
        mock_db.user_exists.return_value = False

        sut = Auth()

        # Act
        result = sut.user_is_authenticated(1)

        # Assert
        assert result is False
        mock_db.user_exists.assert_called_with(1)

    def test_user_is_authenticated_strict(self):
        # Arrange
        sut = Auth()

        # Act
        result = sut.user_is_authenticated_strict(1)

        # Assert
        assert result is True

    def test_user_is_not_authenticated_strict(self):
        # Arrange
        sut = Auth()

        # Act
        result = sut.user_is_authenticated_strict(3)

        # Assert
        assert result is False

    @patch.dict(os.environ, {"LOOKARR_AUTH_PASSWORD": "valid_user"})
    def test_authenticate_valid_user(self):
        # Arrange
        sut = Auth()

        # Act
        result = sut.authenticate_user(1, "valid_user")

        # Assert
        assert result is True
        mock_db.add_user.assert_called_with(1)

    @patch.dict(os.environ, {"LOOKARR_AUTH_PASSWORD": "valid_user"})
    def test_authenticate_invalid_user(self):
        # Arrange
        sut = Auth()

        # Act
        result = sut.authenticate_user(1, "invalid_user")

        # Assert
        assert result is False
