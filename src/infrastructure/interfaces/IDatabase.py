from abc import ABC


class IDatabase(ABC):

    @staticmethod
    def initialise() -> None:
        pass

    @staticmethod
    def add_user(user: int) -> None:
        pass

    @staticmethod
    def user_exists(user: int):
        pass
