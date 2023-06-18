from dataclasses import dataclass
from typing import Optional


@dataclass
class Folder:
    path: Optional[str]
    accessible: Optional[bool]
    freeSpace: Optional[int]
    availableSpace: Optional[str] = None

    def __post_init__(self):
        if self.freeSpace:
            if self.freeSpace > 900000000000:
                self.availableSpace = f"{round(self.freeSpace/(10**12), 2)}TB"
            else:
                self.availableSpace = f"{round(self.freeSpace / (10 ** 9), 2)}GB"
