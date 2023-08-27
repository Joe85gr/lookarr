from abc import ABC, abstractmethod


class IAuth(ABC):
    @abstractmethod
    def user_is_authenticated(self, user_id: int) -> bool:
        """Check if user is authenticated"""

    @abstractmethod
    def authenticate_user(self, user_id, password) -> bool:
        """Authenticates user"""

    @staticmethod
    @abstractmethod
    def user_is_authenticated_strict(user_id: int):
        """Check if user is authenticated in strict mode"""
