import sqlite3
from kink import inject
from src.infrastructure.db.IDatabase import IDatabase


@inject
class Database(IDatabase):
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
