import datetime
from dataclasses import dataclass


@dataclass
class PostureData:
    time: datetime.datetime
    posture_score: float
