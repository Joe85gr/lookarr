import os
from threading import Lock
from src.domain.config.lookarr_config import LookarrConfig
from src.infrastructure.db.sqlite import db


class Auth:
    _instance = None
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if not cls._instance:
                cls._instance = super(Auth, cls).__new__(cls)
                cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        with self._lock:
            if self._initialized:
                return
            self._initialized = True

    @staticmethod
    def user_is_authenticated_strict(user_id: int, config: LookarrConfig):
        if config.strict_mode and user_id not in config.strict_mode_allowed_ids:
            return False
        return True

    @staticmethod
    def user_is_authenticated(user_id: int) -> bool:
        exists = db.user_exists(user_id)
        return True if exists else False

    @staticmethod
    def authenticate_user(user_id, password) -> bool:
        if password == os.environ.get("LOOKARR_AUTH_PASSWORD"):
            db.add_user(user_id)
            return True

        return False


auth = Auth()
