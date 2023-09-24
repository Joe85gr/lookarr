from pydantic import field_validator
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from dataclasses import dataclass
else:
    from pydantic.dataclasses import dataclass

from src.constants import SUPPORTED_LANGUAGES


@dataclass
class LookarrConfig:
    language: str
    strict_mode_allowed_ids: list[int]
    search_all_command: str
    strict_mode: bool = False

    def __post_init__(self) -> None:
        self.strict_mode = True if len(self.strict_mode_allowed_ids) > 0 else False

    @field_validator('language')
    @classmethod
    def language_not_null(cls, value):
        if value not in SUPPORTED_LANGUAGES:
            raise ValueError(f"value must be one of: {''.join(SUPPORTED_LANGUAGES)}")
        return value.title()
