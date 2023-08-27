import pytest

from src.domain.config.lookarr_config import LookarrConfig
from src.constants import SUPPORTED_LANGUAGES


class Test_LookarrConfig:
    def test_valid_config(self):
        # Act
        result = LookarrConfig(
            language="en-us",
            strict_mode_allowed_ids=[],
            search_all_command="Search",
        )

        # Assert
        assert result
        assert result.strict_mode is False

    def test_if_strict_mode_allowed_ids_then_strict_mode_is_true(self):
        # Act
        result = LookarrConfig(
            language="en-us",
            strict_mode_allowed_ids=[1, 2],
            search_all_command="Search",
        )

        # Assert
        assert result.strict_mode is True

    def test_invalid_language(self):
        # Arrange
        expectedErrorMessage = f"value must be one of: {''.join(SUPPORTED_LANGUAGES)}"

        # Assert
        with pytest.raises(ValueError) as result:
            LookarrConfig(
                language="gibberish",
                strict_mode_allowed_ids=[1, 2],
                search_all_command="Search",
            )

        errorMessage = result.value.args[0][0].exc.args[0]
        assert errorMessage == expectedErrorMessage
