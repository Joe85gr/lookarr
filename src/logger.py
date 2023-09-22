import logging
import os
from pathlib import Path

from src.constants import LOG_FULL_PATH


class Logger(logging.Logger):
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
