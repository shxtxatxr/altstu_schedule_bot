import asyncio
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from app.bot.handlers.start import router as start_router
from app.bot.handlers.group import router as group_router
from app.bot.handlers.schedule import router as schedule_router

async def main():
    load_dotenv()

    token = os.getenv("BOT_TOKEN")

    if not token:
        raise RuntimeError("BOT_TOKEN не найден в .env")

    bot = Bot(token=token)
    dp = Dispatcher()

    dp.include_router(start_router)
    dp.include_router(group_router)
    dp.include_router(schedule_router)

    print("Бот запущен")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
