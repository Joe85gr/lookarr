from kink import di
from src.logger import Logger

di[Logger] = Logger(__name__)
