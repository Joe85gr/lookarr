from kink import di
from src.logger import Logger
from warnings import filterwarnings
from telegram.warnings import PTBUserWarning

filterwarnings(action="ignore", message=r".*CallbackQueryHandler", category=PTBUserWarning)
di[Logger] = Logger(__name__)
