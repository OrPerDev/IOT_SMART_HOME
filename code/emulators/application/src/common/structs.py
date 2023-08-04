from dataclasses import dataclass
from typing import Optional
import time


@dataclass(frozen=False)
class AudioRecord:
    audio_data: bytes
    # has defaults
    id: Optional[int] = None
    name: Optional[str] = None
    timestamp: Optional[int] = None

    def __post_init__(self):
        # default timestamp to current time
        if self.timestamp is None:
            self.timestamp = int(time.time())
        # default name to Recording_<timestamp>
        if self.name is None:
            self.name = f"Recording_{self.timestamp}"
