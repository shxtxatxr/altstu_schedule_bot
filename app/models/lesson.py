from dataclasses import dataclass
from datetime import date, time


@dataclass
class Lesson:
    date: date
    start_time: time
    end_time: time
    subject: str
    lesson_type: str | None
    room: str | None
    teacher: str | None
    teacher_position: str | None
    group: str
    week_number: int | None
    is_once: bool