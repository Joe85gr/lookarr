from src.constants import LOOKAR_DB_PATH
from src.infrastructure.interfaces.IDatabase import IDatabase
from tinydb import TinyDB, Query


class TinyDb(IDatabase):
    @staticmethod
    def initialise() -> None:
        TinyDB(f"{LOOKAR_DB_PATH}")

    @staticmethod
    def add_user(user: int) -> None:
        with TinyDB(f"{LOOKAR_DB_PATH}") as db:
            db.insert({"chat_id": user})

    @staticmethod
    def user_exists(user_id: int):
        with TinyDB(f"{LOOKAR_DB_PATH}") as db:
            return db.contains(Query().chat_id == user_id)
