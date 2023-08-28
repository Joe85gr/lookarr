import os
from unittest.mock import patch, MagicMock
from kink import di

from src.infrastructure.interfaces.IDatabase import IDatabase
from src.domain.auth.authentication import Auth


mock_db = MagicMock()
di[IDatabase] = mock_db


class Test_Auth:
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
