import sqlite3
from threading import Lock
from src.infrastructure.db.IDatabase import IDatabase


class Database(IDatabase):
    _instance = None
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if not cls._instance:
                cls._instance = super(Database, cls).__new__(cls)
                cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        with self._lock:
            if self._initialized:
                return
            self._initialized = True

    @staticmethod
    def initialise() -> None:
        with sqlite3.connect("user_config/lookar.db") as con:
            cur = con.cursor()

            cur.execute(""" CREATE TABLE IF NOT EXISTS AUTHENTICATED_USERS (
                            id INTEGER PRIMARY KEY AUTOINCREMENT, 
                            chat_id INTEGER UNIQUE);
                        """)

    @staticmethod
    def add_user(user: int) -> None:
        with sqlite3.connect("user_config/lookar.db") as con:
            cur = con.cursor()
            data = (user, )
            cur.execute(f""" INSERT INTO AUTHENTICATED_USERS (chat_id)
                            VALUES (?)
                        """, data)

    @staticmethod
    def user_exists(user: int):
        with sqlite3.connect("user_config/lookar.db") as con:
            cur = con.cursor()
            data = (user, )
            cur.execute(f""" SELECT * FROM AUTHENTICATED_USERS
                             WHERE chat_id = (?)
                        """, data)
            return cur.fetchone()


db = Database()
