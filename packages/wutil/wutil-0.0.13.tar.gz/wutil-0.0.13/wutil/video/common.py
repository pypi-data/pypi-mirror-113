from dataclasses import dataclass
from typing import List

import numpy as np


@dataclass
class Frame(object):
    data: np.ndarray
    idx: int
    time: float


@dataclass
class FrameGroup(object):
    frames: List[Frame]

    @property
    def last_frame(self):
        return self.frames[-1]

    def __len__(self):
        return len(self.frames)
