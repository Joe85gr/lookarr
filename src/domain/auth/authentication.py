import os

from kink import inject

from src.domain.auth.interfaces.iauthentication import IAuth
from src.domain.config.app_config import Config
from src.infrastructure.interfaces.IDatabase import IDatabase


@inject
class Auth(IAuth):
    def __init__(self, db: IDatabase, config: Config):
        self._db = db
        self._config = config.lookarr

    def user_is_authenticated_strict(self, user_id: int):
        if self._config.strict_mode and user_id not in self._config.strict_mode_allowed_ids:
            return False
        return True

    def user_is_authenticated(self, user_id: int) -> bool:
        exists = self._db.user_exists(user_id)
        return True if exists else False

    def authenticate_user(self, user_id, password) -> bool:
        if password == os.environ.get("LOOKARR_AUTH_PASSWORD"):
            self._db.add_user(user_id)
            return True

        return False
