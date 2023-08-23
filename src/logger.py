import logging
import os
from pathlib import Path

from src.constants import LOG_FULL_PATH


class Logger(object):
    _instance = None
    logger = None

    def __new__(cls, name: str = None):
        if cls._instance is None:
            if name is None:
                raise ValueError("Logger name cannot be None")
            cls._instance = super(Logger, cls).__new__(cls)
            cls.logger = cls.get_logger(name)
            cls.logger.info('Created logger')
        return cls.logger

    @staticmethod
    def get_logger(name: str = None) -> logging.Logger:
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)

        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(module)s - %(message)s")

        relative_log_full_path = f"{Path(__file__).parent.resolve()}/{LOG_FULL_PATH}"
        relative_log_path = Path(relative_log_full_path).parent.resolve()

        if not os.path.exists(relative_log_path):
            os.makedirs(relative_log_path)

        file_handler = logging.FileHandler(relative_log_full_path)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        return logger
