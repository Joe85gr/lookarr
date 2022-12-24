import os

import pytest

from src.domain.validators.env_validator import EnvValidator


class Test_EnvValidator:
    @pytest.fixture(autouse=True)
    def before_each(self):
        os.environ.clear()

    def test_env_variables_are_set(self):
        # Arrange
        os.environ["TELEGRAM_BOT_KEY"] = "some-bot-key"
        os.environ["LOOKARR_AUTH_PASSWORD"] = "some-addarr-password"

        # Act
        result = EnvValidator({})
        result.verify_required_env_variables_exist()

        # Assess
        assert result.is_valid is True

    def test_env_variables_are_not_set(self):
        # Arrange

        # Act
        result = EnvValidator({})
        result.verify_required_env_variables_exist()

        # Assess
        assert result.is_valid is False
