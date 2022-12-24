import os

from src.infrastructure.sqlite import IDatabase
from src.app.config.all_config import Config


class Auth:
    def __init__(self, db: IDatabase) -> None:
        self.db = db

    @staticmethod
    def user_is_authenticated_strict(user_id: int, config: Config):
        if config.lookarr.strict_mode:
            return True if user_id in config.lookarr.strict_mode_allowed_ids else False
        return True

    def user_is_authenticated(self, user_id: int) -> bool:
        exists = self.db.user_exists(user_id)
        return True if exists else False

    def authenticate_user(self, user_id, password) -> bool:
        if password == os.environ.get("LOOKARR_AUTH_PASSWORD"):
            self.db.add_user(user_id)
            return True

        return False
