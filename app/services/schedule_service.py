from app.models.lesson import Lesson
from app.parsers.altstu_parser import parse_schedule
from app.providers.altstu import get_schedule_page


async def get_group_schedule(group_id: str) -> list[Lesson]:
    """
    Получает расписание группы с сайта АлтГТУ
    и преобразует HTML в список Lesson.
    """

    html = await get_schedule_page(group_id)

    return parse_schedule(html)