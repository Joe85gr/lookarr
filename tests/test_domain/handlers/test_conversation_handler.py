from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

from tests.mockers.mock_decorators import mock_check_user_is_authenticated, mock_check_check_conversation

mock_check_user_is_authenticated()
mock_check_check_conversation()

from src.domain.config.app_config import ConfigLoader
from src.domain.handlers.conversation_handler import SearchHandler
from src.interface.keyboard import Keyboard


class Test_SearchHandler:
    @patch.object(SearchHandler, 'show_medias', MagicMock())
    def test_option_change(self):
        # Arrange
        update = Mock()
        context = Mock()
        update.callback_query = Mock()
        path = f"{Path(__file__).parent.parent.parent}/data/config.yml"
        ConfigLoader(path)

        test_cases = [
            {"query": "Next", "expected_result": 3},
            {"query": "Previous", "expected_result": 1},
        ]

        for test_case in test_cases:
            context.user_data = {"position": 2}
            update.callback_query.data = test_case["query"]

            sut = SearchHandler(Mock(), Keyboard())

            # Act
            sut.change_option(update, context)

            # Assert
            assert context.user_data["position"] == test_case["expected_result"]
