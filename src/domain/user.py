from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from dataclasses import dataclass
else:
    from pydantic.dataclasses import dataclass


@dataclass
class UserReply:
    reply: str
    value: str = ""
    is_valid: bool = False

    def __post_init__(self) -> None:
        command = self.reply.lower().split(" ")[0]
        self.value = self.reply.replace(command, "").strip()
        self.is_valid = True if self.value else False

