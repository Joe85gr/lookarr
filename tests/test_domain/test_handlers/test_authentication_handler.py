from logging import Logger
from unittest.mock import MagicMock, AsyncMock
import pytest
from kink import di
from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

from src import ILogger
from src.domain.auth.interfaces.iauthentication import IAuth
from src.domain.handlers.authentication_handler import AuthHandler


class TestAuthHandler:

    @pytest.fixture(autouse=True)
    def setup_method(self):
        self.update = MagicMock(autospec=Update)
        self.update.message.reply_text = AsyncMock()
        self.context = AsyncMock(spec=CallbackContext)
        self._auth = MagicMock()
        self._logger = MagicMock(spec=Logger)

        di[IAuth] = self._auth
        di[ILogger] = self._logger

    @pytest.mark.asyncio
    async def test_authorised(self):
        self.update.effective_user.id = 123

        self._auth.user_is_authenticated_strict.awaited_return_value = True
        self._auth.user_is_authenticated.return_value = False
        self._auth.authenticate_user.awaited_return_value = True

        sut = AuthHandler()

        result = await sut.authenticate(self.update, self.context)
        self.update.message.reply_text.assert_awaited_once_with(text=f"Nice one! You're in buddy 😌")

    @pytest.mark.asyncio
    async def test_unauthorised_user(self):
        # Arrange
        self.update.effective_user.id = 123
        self._auth.user_is_authenticated_strict.return_value = False

        sut = AuthHandler()

        # Act
        result = await sut.authenticate(self.update, self.context)

        # Assert
        self._logger.info.assert_called_with("unauthorised user 123. Won't reply :D")
        assert result == ConversationHandler.END

    @pytest.mark.asyncio
    async def test_already_authenticated_user(self):
        self.update.effective_user.id = 123

        self._auth.user_is_authenticated_strict.return_value = True
        self._auth.user_is_authenticated.return_value = True

        sut = AuthHandler()

        await sut.authenticate(self.update, self.context)
        self.update.message.reply_text.assert_awaited_once_with(
            text="What you want?? You're already authenticated! Do you like passwords or something 🤣")

    @pytest.mark.asyncio
    async def test_invalid_user_reply(self):
        self.update.effective_user.id = 123
        self.update.message.text = "invalid"

        self._auth.user_is_authenticated_strict.return_value = True
        self._auth.user_is_authenticated.return_value = False

        sut = AuthHandler()

        await sut.authenticate(self.update, self.context)
        self.update.message.reply_text.assert_awaited_once_with(
            text="You need to write /auth <password> 😒 don't make me repeat myself..")

    @pytest.mark.asyncio
    async def test_wrong_password(self):
        self.update.effective_user.id = 123

        self._auth.user_is_authenticated_strict.return_value = True
        self._auth.user_is_authenticated.return_value = False
        self._auth.authenticate_user.return_value = False

        sut = AuthHandler()

        await sut.authenticate(self.update, self.context)
        self.update.message.reply_text.assert_awaited_once_with(
            text=f"Sorry pal, wrong password 😝 try again.")
