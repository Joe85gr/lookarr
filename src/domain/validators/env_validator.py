from os import environ


class EnvValidator:
    def __init__(self, values: dict = None) -> None:
        self.values = values
        self.reasons = []
        self.is_valid = False

    def verify_required_env_variables_exist(self, radarr_is_enabled: bool, sonarr_is_enabled: bool):
        self.is_valid = True
        self.reasons = []

        requiredEnv = ["TELEGRAM_BOT_KEY", "LOOKARR_AUTH_PASSWORD"]
        if radarr_is_enabled:
            requiredEnv.append("RADARR_API_KEY")

        if sonarr_is_enabled:
            requiredEnv.append("SONARR_API_KEY")

        for envKey in requiredEnv:
            if environ.get(envKey) is None:
                self.is_valid = False
                self.reasons.append(envKey)
