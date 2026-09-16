from datetime import date, timedelta
from app.models.lesson import Lesson


WEEKDAYS = {
    0: "Понедельник",
    1: "Вторник",
    2: "Среда",
    3: "Четверг",
    4: "Пятница",
    5: "Суббота",
    6: "Воскресенье",
}


LESSON_TYPES = {
    "л.": "лекция",
    "пр.": "практика",
    "л.р.": "лабораторная работа",
}


def format_day_schedule(
    lessons: list[Lesson],
    target_date: date,
    group_name: str,
) -> str:
    day_lessons = [
        lesson
        for lesson in lessons
        if lesson.date == target_date
    ]

    weekday = WEEKDAYS[target_date.weekday()]

    header = (
        f"📚 Группа: {group_name}\n"
        f"📅 {weekday} {target_date.strftime('%d.%m.%Y')}"
    )

    if not day_lessons:
        return (
            f"{header}\n\n"
            "Занятий нет."
        )

    day_lessons.sort(
        key=lambda lesson: lesson.start_time
    )

    lines = [header, ""]

    for index, lesson in enumerate(day_lessons, start=1):
        time_range = (
            f"{lesson.start_time.strftime('%H:%M')}"
            f"–"
            f"{lesson.end_time.strftime('%H:%M')}"
        )

        lesson_type = LESSON_TYPES.get(
            lesson.lesson_type,
            lesson.lesson_type,
        )

        subject = lesson.subject

        lines.append(
            f"{index}. {time_range} — {subject}"
        )

        if lesson_type:
            lines.append(
                f"   Тип: {lesson_type}"
            )

        if lesson.room:
            lines.append(
                f"   Аудитория: {lesson.room}"
            )

        if lesson.teacher:
            teacher = lesson.teacher

            if lesson.teacher_position:
                teacher += (
                    f", {lesson.teacher_position}"
                )

            lines.append(
                f"   Преподаватель: {teacher}"
            )

        lines.append("")

    return "\n".join(lines).rstrip()
def format_week_schedule(
    lessons: list[Lesson],
    start_date: date,
    group_name: str,
) -> str:
    """
    Формирует расписание на неделю начиная с понедельника.
    """

    end_date = start_date + timedelta(days=6)

    lines = [
        f"📚 Группа: {group_name}",
        (
            f"📋 Неделя: "
            f"{start_date.strftime('%d.%m.%Y')}–"
            f"{end_date.strftime('%d.%m.%Y')}"
        ),
        "",
    ]

    for day_offset in range(7):
        current_date = start_date + timedelta(days=day_offset)

        weekday = WEEKDAYS[current_date.weekday()]

        day_lessons = [
            lesson
            for lesson in lessons
            if lesson.date == current_date
        ]

        lines.append(
            f"📅 {weekday} {current_date.strftime('%d.%m.%Y')}"
        )

        if not day_lessons:
            lines.append("   Занятий нет.")
            lines.append("")
            continue

        day_lessons.sort(key=lambda lesson: lesson.start_time)

        for index, lesson in enumerate(day_lessons, start=1):
            time_range = (
                f"{lesson.start_time.strftime('%H:%M')}"
                f"–"
                f"{lesson.end_time.strftime('%H:%M')}"
            )

            lesson_type = LESSON_TYPES.get(
                lesson.lesson_type,
                lesson.lesson_type,
            )

            lines.append(
                f"   {index}. {time_range} — {lesson.subject}"
            )

            if lesson_type:
                lines.append(
                    f"      Тип: {lesson_type}"
                )

            if lesson.room:
                lines.append(
                    f"      Аудитория: {lesson.room}"
                )

            if lesson.teacher:
                teacher = lesson.teacher

                if lesson.teacher_position:
                    teacher += f", {lesson.teacher_position}"

                lines.append(
                    f"      Преподаватель: {teacher}"
                )

        lines.append("")

    return "\n".join(lines).rstrip()