from kink import di
from unittest.mock import Mock, patch, MagicMock

from src.domain.checkers.idefaults_checker import IDefaultValuesChecker
from tests.mockers.mock_decorators import mock_check_user_is_authenticated, mock_check_check_conversation

mock_check_user_is_authenticated()
mock_check_check_conversation()

from src.domain.handlers.handler import Handler


class Test_SearchHandler:
    @patch.object(Handler, 'show_medias', MagicMock())
    def test_option_change(self):
        # Arrange
        di[IDefaultValuesChecker] = Mock()
        update = Mock()
        context = Mock()
        update.callback_query = Mock()

        test_cases = [
            {"query": "Next", "expected_result": 3},
            {"query": "Previous", "expected_result": 1},
        ]

        for test_case in test_cases:
            context.user_data = {"position": 2}
            update.callback_query.data = test_case["query"]

            sut = Handler(Mock())

            # Act
            sut.change_option(update, context)

            # Assert
            assert context.user_data["position"] == test_case["expected_result"]
