from abc import ABC, abstractmethod


class IDatabase(ABC):

    @staticmethod
    @abstractmethod
    def initialise() -> None:
        pass

    @staticmethod
    @abstractmethod
    def add_user(user: int) -> None:
        pass

    @staticmethod
    @abstractmethod
    def user_exists(user: int):
        pass
