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
    tag: str
    start_time: Optional[TimeInfo] = None
    end_time: Optional[TimeInfo] = None
    duration: Optional[int] = None
    calendar_event_id: Optional[str] = None
    priority: Optional[int] = None
    attendees: Optional[list[str]] = field(default_factory=list)
