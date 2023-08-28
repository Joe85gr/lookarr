from kink import di
from src.logger import ILogger, Logger

di[ILogger] = Logger(__name__)
