from abc import ABC

from src.domain.handlers.interfaces.imedia_handler import IMediaHandler


class IMovieHandler(IMediaHandler, ABC):
    """Movie handler interface"""
