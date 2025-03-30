from dataclasses import dataclass, field
import datetime
from typing import Optional


@dataclass
class TimeInfo:
    date_time: datetime
    time_zone: str

@dataclass
class Task:
    name: str
    start_time: TimeInfo
    end_time: TimeInfo
    priority: Optional[int] = None
    description: Optional[str] = None
    attendees: Optional[list[str]] = field(default_factory=list)
