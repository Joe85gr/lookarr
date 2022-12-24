from os import environ
from src.domain.validators.base_validator import BaseValidator


class EnvValidator(BaseValidator):
    def verify_required_env_variables_exist(self):
        self.is_valid = True
        self.reasons = []

        requiredEnv = ["TELEGRAM_BOT_KEY", "LOOKARR_AUTH_PASSWORD"]

        for envKey in requiredEnv:
            if environ.get(envKey) is None:
                self.is_valid = False
                self.reasons.append(envKey)
