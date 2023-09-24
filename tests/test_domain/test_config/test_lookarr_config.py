from src.domain.config.lookarr_config import LookarrConfig


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
