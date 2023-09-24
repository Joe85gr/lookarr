from pydantic import field_validator
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from dataclasses import dataclass
else:
    from pydantic.dataclasses import dataclass

from src.constants import SUPPORTED_LANGUAGES


@dataclass
class LookarrConfig:
    language: SUPPORTED_LANGUAGES
    strict_mode_allowed_ids: list[int]
    search_all_command: str
    strict_mode: bool = False

    def __post_init__(self) -> None:
        self.strict_mode = True if len(self.strict_mode_allowed_ids) > 0 else False

