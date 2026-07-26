import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

# Для прокси
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from dotenv import load_dotenv

# База данных
from db import DataBase

# Импорт роутеров
from handlers import commands_router, ftext_filters_router, messages_router

# Логирование
from setup_logging import logger

# Загрузка файла .env и получение токена
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    logger.error("BOT_TOKEN не найден! Проверьте .env файл")
    exit(1)

# Загрузка прокси
PROXY = os.getenv("BOT_PROXY")
if not PROXY:
    logger.error("BOT_PROXY не найден! Проверьте .env файл")
    exit(1)

# Вписать тип, адрес и порт прокси
session = AiohttpSession(proxy=PROXY)

# Настройки бота
bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    session=session,
)

# Создаем 1 экземпляр БД
db = DataBase()
# Подключение диспетчера
dp = Dispatcher()

# Сохраняем БД в диспетчере
dp["db"] = db

# Здесь разместить подключение роутеров
dp.include_router(commands_router)
dp.include_router(messages_router)
dp.include_router(ftext_filters_router)


# Основная функция
async def main():
    await db.init_db()
    logger.info("Бот запущен!")
    await dp.start_polling(bot)


# Проверка на запуск извне
if __name__ == "__main__":
    asyncio.run(main())
