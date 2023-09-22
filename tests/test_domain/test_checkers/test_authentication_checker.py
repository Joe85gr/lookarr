import pytest
from kink import di
from unittest.mock import MagicMock
from telegram import User
from telegram.ext import ConversationHandler
from src.domain.auth.interfaces.iauthentication import IAuth
from src.domain.checkers.authentication_checker import check_user_is_authenticated
from src.logger import Logger


class TestCheckUserIsAuthenticated:
    @pytest.fixture(autouse=True)
    def setup_method(self):
        self.update = MagicMock()
        self.context = MagicMock()
        self.func = MagicMock()

        self._mock_auth = MagicMock()
        self._mock_logger = MagicMock()

        di[IAuth] = self._mock_auth
        di[Logger] = self._mock_logger

    def test_unauthorised_user(self):
        # Arrange
        unauthenticated_user = User(id=123456, first_name='Mocked User', is_bot=False)

        self.update.effective_user = unauthenticated_user
        self._mock_auth.user_is_authenticated_strict.return_value = False

        # Act
        result = check_user_is_authenticated(self.func)(self, self.update, self.context)

        # Assert
        self._mock_logger.info.assert_called_with("unauthorised user 123456")
        assert result == ConversationHandler.END

    def test_not_authenticated_user(self):
        # Arrange
        not_auth_user = User(id=7890, first_name='Mocked User 2', is_bot=False)

        self.update.effective_user = not_auth_user
        self.update.message = MagicMock()
        self._mock_auth.user_is_authenticated_strict.return_value = True
        self._mock_auth.user_is_authenticated.return_value = False

        # Act
        result = check_user_is_authenticated(self.func)(self, self.update, self.context)

        # Assert
        self.update.message.reply_text.assert_called_with(
            "Well, shit! 😄 seems you're not authenticated! Write /auth <password> to authenticate!")
        assert result == ConversationHandler.END

    def test_authenticated_user(self):
        # Arrange
        auth_user = User(id=54321, first_name='Mocked User 3', is_bot=False)

        self.update.effective_user = auth_user
        self._mock_auth.user_is_authenticated_strict.return_value = True
        self._mock_auth.user_is_authenticated.return_value = True

        # Act
        check_user_is_authenticated(self.func)(self, self.update, self.context)

        # Assert
        self.func.assert_called_once_with(self, self.update, self.context)
