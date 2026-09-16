import re
from datetime import date, datetime, time

from bs4 import BeautifulSoup

from app.models.lesson import Lesson


WEEK_PATTERN = re.compile(
    r"(\d{2}\.\d{2}\.\d{4})\s*-\s*"
    r"(\d{2}\.\d{2}\.\d{4})\s*"
    r"\((\d+)\s*неделя\)"
)

TIME_PATTERN = re.compile(
    r"(\d{2}:\d{2})\s*-\s*(\d{2}:\d{2})"
)


def parse_date(value: str) -> date:
    return datetime.strptime(value, "%d.%m.%Y").date()


def parse_time(value: str) -> time:
    return datetime.strptime(value, "%H:%M").time()


def parse_time_range(value: str) -> tuple[time, time]:
    match = TIME_PATTERN.search(value)

    if not match:
        raise ValueError(f"Не удалось распознать время: {value}")

    start_time = parse_time(match.group(1))
    end_time = parse_time(match.group(2))

    return start_time, end_time


def parse_lesson_type(text: str) -> str | None:
    match = re.search(r"\((л\.р\.|л\.|пр\.)\)", text)

    if not match:
        return None

    return match.group(1)


def clean_subject(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()

    text = re.sub(
        r"\s*\((л\.р\.|л\.|пр\.)\)\s*$",
        "",
        text,
    )

    return text


def parse_teacher(cell) -> tuple[str | None, str | None]:
    if cell is None:
        return None, None

    nobr = cell.find("nobr")

    teacher = None

    if nobr:
        teacher = nobr.get_text(" ", strip=True)

    position = None

    span = cell.find("span")

    if span:
        position = span.get_text(" ", strip=True)

    return teacher, position


def parse_schedule(html: str) -> list[Lesson]:
    soup = BeautifulSoup(html, "lxml")

    schedule = soup.select_one("div.schedule")

    if schedule is None:
        raise ValueError("Блок div.schedule не найден")

    group_element = schedule.select_one("div.group")

    if group_element is None:
        raise ValueError("Название группы не найдено")

    group_text = group_element.get_text(" ", strip=True)

    group_match = re.search(
        r"Группа:\s*(.+)",
        group_text,
    )

    if not group_match:
        raise ValueError(
            f"Не удалось определить группу: {group_text}"
        )

    group = group_match.group(1).strip()

    lessons: list[Lesson] = []

    current_week_number: int | None = None
    current_date: date | None = None

    for element in schedule.find_all(["h3", "th", "tr"]):

        # -----------------------------------------
        # Заголовок недели
        # -----------------------------------------
        if element.name == "h3":
            text = element.get_text(" ", strip=True)

            week_match = WEEK_PATTERN.search(text)

            if week_match:
                current_week_number = int(
                    week_match.group(3)
                )

            continue

        # -----------------------------------------
        # Заголовок дня
        # -----------------------------------------
        if element.name == "th" and "day" in element.get("class", []):
            text = element.get_text(" ", strip=True)

            date_match = re.search(
                r"(\d{2}\.\d{2}\.\d{4})",
                text,
            )

            if date_match:
                current_date = parse_date(
                    date_match.group(1)
                )

            continue

        # -----------------------------------------
        # Строка занятия
        # -----------------------------------------
        if element.name != "tr":
            continue

        if current_date is None:
            continue

        cells = element.find_all("td", recursive=False)

        if len(cells) < 2:
            continue

        time_text = cells[0].get_text(" ", strip=True)

        if not TIME_PATTERN.search(time_text):
            continue

        try:
            start_time, end_time = parse_time_range(
                time_text
            )
        except ValueError:
            continue

        subject_cell = cells[1]

        subject_raw = subject_cell.get_text(
            " ",
            strip=True,
        )

        if not subject_raw:
            continue

        lesson_type = parse_lesson_type(subject_raw)
        subject = clean_subject(subject_raw)

        room = None

        if len(cells) >= 3:
            room_text = cells[2].get_text(
                " ",
                strip=True,
            )

            if room_text:
                room = room_text

        teacher = None
        teacher_position = None

        teacher_cell = element.select_one(
            "td.teacher"
        )

        if teacher_cell:
            teacher, teacher_position = parse_teacher(
                teacher_cell
            )

        is_once = "once" in element.get("class", [])

        lessons.append(
            Lesson(
                date=current_date,
                start_time=start_time,
                end_time=end_time,
                subject=subject,
                lesson_type=lesson_type,
                room=room,
                teacher=teacher,
                teacher_position=teacher_position,
                group=group,
                week_number=current_week_number,
                is_once=is_once,
            )
        )

    return lessons