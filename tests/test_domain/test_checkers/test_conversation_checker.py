import pytest
from unittest.mock import MagicMock, AsyncMock
from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

from src.domain.checkers.conversation_checker import check_conversation, answer_query
from src.domain.handlers.stop_handler import stop_handler


@pytest.mark.asyncio
class TestCheckConversation:
    @pytest.fixture(autouse=True)
    def setup_method(self):
        self.update = AsyncMock(autospec=Update)
        self.context = AsyncMock(spec=CallbackContext)
        self.cls = AsyncMock()
        self.func = MagicMock()
        stop_handler.lost_track_of_conversation = AsyncMock(return_value=False)

    @pytest.mark.asyncio
    async def test_check_conversation_without_lost_track(self):
        # Arrange
        sut = check_conversation([])(self.func)

        stop_handler.lost_track_of_conversation.return_value = False

        # Act
        result = await sut(self.cls, self.update, self.context)

        # Assert
        self.func.assert_called_once_with(self.cls, self.update, self.context)
        assert result == self.func.return_value

    @pytest.mark.asyncio
    async def test_check_conversation_with_lost_track(self):
        # Arrange
        sut = check_conversation([])(self.func)

        stop_handler.lost_track_of_conversation.return_value = True

        # Act
        result = await sut(self.cls, self.update, self.context)

        # Assert
        self.func.assert_not_called()
        assert result == ConversationHandler.END


class TestAnswerQuery:
    @pytest.fixture(autouse=True)
    def setup_method(self):
        self.update = MagicMock(autospec=Update)
        self.context = MagicMock(spec=CallbackContext)
        self.cls = MagicMock()
        self.func = MagicMock()

    def test_answer_query_calls_func(self):
        # Arrange
        aq = answer_query()
        sut = aq(self.func)

        # Act
        result = sut(self.cls, self.update, self.context)

        # Assert
        self.update.callback_query.answer.assert_called_once()
        self.func.assert_called_once_with(self.cls, self.update, self.context)
        assert result == self.func.return_value
