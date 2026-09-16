import os

import asyncpg
from dotenv import load_dotenv

load_dotenv()

DATABASE_CONFIG = {
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT", 5432)),
}


async def get_connection():
    return await asyncpg.connect(**DATABASE_CONFIG)