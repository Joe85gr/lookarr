import logging
from src.constants import LOG_FULL_PATH


logger = logging.getLogger()
logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(module)s - %(message)s")
file_handler = logging.FileHandler(LOG_FULL_PATH)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
