import logging
import os
from abc import ABC, abstractmethod
from pathlib import Path

from src.constants import LOG_FULL_PATH


class ILogger(ABC):
    @abstractmethod
    def info(self, message: str) -> None:
        """Logs an info message"""

    @abstractmethod
    def debug(self, message: str) -> None:
        """Logs a debug message"""

    @abstractmethod
    def warning(self, message: str) -> None:
        """Logs a warning message"""

    @abstractmethod
    def error(self, message: str, e: Exception = None) -> None:
        """Logs an error message"""

    @abstractmethod
    def critical(self, message: str) -> None:
        """Logs a critical message"""

    @abstractmethod
    def exception(self, message: str) -> None:
        """Logs an exception message"""

    @abstractmethod
    def log(self, level: int, message: str) -> None:
        """Logs a message at a given level"""


class Logger(logging.Logger, ILogger):
    def __init__(self, name: str):
        super().__init__(name)
        super().setLevel(logging.INFO)

        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(module)s - %(message)s")

        relative_log_full_path = f"{Path(__file__).parent.resolve()}/{LOG_FULL_PATH}"
        relative_log_path = Path(relative_log_full_path).parent.resolve()

        if not os.path.exists(relative_log_path):
            os.makedirs(relative_log_path)

        file_handler = logging.FileHandler(relative_log_full_path)
        file_handler.setFormatter(formatter)
        super().addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        super().addHandler(console_handler)
