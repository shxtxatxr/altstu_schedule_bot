from datetime import date, timedelta

from aiogram import F, Router
from aiogram.types import Message

from app.formatters.schedule import (
    format_day_schedule,
    format_week_schedule,
)
from app.services.schedule_service import get_group_schedule

from app.repositories.user_repository import get_user_group
router = Router()


async def send_day_schedule(
    message: Message,
    target_date: date,
):
    user_id = message.from_user.id

    group = await get_user_group(user_id)
    if not group:
        await message.answer(
            "Учебная группа не выбрана.\n\n"
            "Сначала выберите «⚙️ Изменить группу»."
        )
        return

    group_id = group["external_id"]
    group_name = group["name"]

    lessons = await get_group_schedule(group_id)

    text = format_day_schedule(
        lessons,
        target_date,
        group_name,
    )

    await message.answer(text)


@router.message(F.text == "📅 Сегодня")
async def today_schedule(message: Message):
    today = date.today()

    await send_day_schedule(
        message,
        today,
    )


@router.message(F.text == "➡️ Завтра")
async def tomorrow_schedule(message: Message):
    tomorrow = date.today() + timedelta(days=1)

    await send_day_schedule(
        message,
        tomorrow,
    )

@router.message(F.text == "📋 Неделя")
async def week_schedule(message: Message):
    user_id = message.from_user.id

    group = await get_user_group(user_id)
    if not group:
        await message.answer(
            "Учебная группа не выбрана.\n\n"
            "Сначала выберите «⚙️ Изменить группу»."
        )
        return

    group_id = group["external_id"]
    group_name = group["name"]

    lessons = await get_group_schedule(group_id)

    today = date.today()

    # Находим понедельник текущей недели
    monday = today - timedelta(days=today.weekday())

    text = format_week_schedule(
        lessons,
        monday,
        group_name,
    )

    await message.answer(text)

@router.message(F.text == "➡️ Следующая неделя")
async def next_week_schedule(message: Message):
    user_id = message.from_user.id

    group = await get_user_group(user_id)
    if not group:
        await message.answer(
            "Учебная группа не выбрана.\n\n"
            "Сначала выберите «⚙️ Изменить группу»."
        )
        return

    group_id = group["external_id"]
    group_name = group["name"]

    lessons = await get_group_schedule(group_id)

    today = date.today()

    # Понедельник текущей недели
    current_monday = today - timedelta(days=today.weekday())

    # Понедельник следующей недели
    next_monday = current_monday + timedelta(days=7)

    text = format_week_schedule(
        lessons,
        next_monday,
        group_name,
    )

    await message.answer(text)

@router.message(F.text == "🔄 Обновить расписание")
async def refresh_schedule(message: Message):
    user_id = message.from_user.id

    group = await get_user_group(user_id)
    if not group:
        await message.answer(
            "Учебная группа не выбрана.\n\n"
            "Сначала выберите «⚙️ Изменить группу»."
        )
        return

    group_id = group["external_id"]
    group_name = group["name"]

    try:
        # Повторно получаем актуальное расписание с сайта АлтГТУ
        lessons = await get_group_schedule(group_id)

        # Пока расписание не сохраняем в отдельный кэш.
        # Сам факт повторного запроса является обновлением.

        await message.answer(
            f"🔄 Расписание обновлено.\n\n"
            f"📚 Группа: {group_name}\n"
            f"Загружено занятий: {len(lessons)}"
        )

    except Exception:
        await message.answer(
            "Не удалось обновить расписание.\n\n"
            "Проверьте подключение к интернету и попробуйте ещё раз."
        )

@router.message(F.text == "ℹ️ Помощь")
async def help_handler(message: Message):
    await message.answer(
        "ℹ️ Помощь\n\n"
        "Бот показывает расписание занятий АлтГТУ.\n\n"
        "📅 Сегодня — расписание на сегодня\n"
        "➡️ Завтра — расписание на завтра\n"
        "📋 Неделя — расписание текущей недели\n"
        "➡️ Следующая неделя — расписание следующей недели\n"
        "⚙️ Изменить группу — выбрать другую учебную группу\n"
        "🔄 Обновить расписание — заново загрузить данные с сайта АлтГТУ"
    )