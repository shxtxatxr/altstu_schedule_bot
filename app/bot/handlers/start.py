from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.repositories.user_repository import get_user_group


router = Router()


@router.message(Command("start"))
async def start_handler(message: Message):

    group = await get_user_group(
        message.from_user.id
    )

    if group:
        await message.answer(
            f"С возвращением.\n\n"
            f"Ваша группа: {group['name']}\n\n"
            "Используйте кнопки меню для работы с расписанием."
        )
    else:
        await message.answer(
            "Добро пожаловать.\n\n"
            "Учебная группа ещё не выбрана.\n"
            "Нажмите «⚙️ Изменить группу»."
        )