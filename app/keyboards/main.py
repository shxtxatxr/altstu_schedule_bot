from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def main_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📅 Сегодня"),
                KeyboardButton(text="➡️ Завтра"),
            ],
            [
                KeyboardButton(text="📋 Неделя"),
                KeyboardButton(text="➡️ Следующая неделя"),
            ],
            [
                KeyboardButton(text="⚙️ Изменить группу"),
                KeyboardButton(text="🔄 Обновить расписание"),
            ],
            [
                KeyboardButton(text="ℹ️ Помощь"),
            ],
        ],
        resize_keyboard=True,
    )