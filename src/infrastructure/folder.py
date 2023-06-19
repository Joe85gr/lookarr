from dataclasses import dataclass
from typing import Optional


@dataclass
class Folder:
    path: Optional[str]
    accessible: Optional[bool]
    freeSpace: Optional[int]

    @property
    def availableSpace(self):
        if self.freeSpace:
            if self.freeSpace > 900000000000:
                return f"{round(self.freeSpace/(10**12), 2)}TB"
            else:
                return f"{round(self.freeSpace / (10 ** 9), 2)}GB"

