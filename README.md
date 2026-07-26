# 💧 Water Tracker Telegram Bot

Асинхронный Telegram-бот для расчета индивидуальной нормы воды и трекинга ежедневного водного баланса.

## 🛠 Технологический стек

* **Python 3.11+**
* **aiogram 3.x** - асинхронный фреймворк для Telegram Bot API (FSM, Routers, Keyboards)
* **SQLAlchemy 2.0 (AsyncORM) + aiosqlite** - асинхронная работа с базой данных SQLite
* **Pydantic v2** - строгая валидация и обработка пользовательского ввода
* **Docker** - контейнеризация проекта для быстрого деплоя
* **python-dotenv** - управление конфигурацией и секретами через файл `.env`

## ⚙️ Функционал

* Расчет индивидуальной суточной нормы воды на основе веса пользователя.
* Быстрое добавление выпитого объема через интерфейсные кнопки.
* Наглядный прогресс-бар выпитой воды за текущий день.
* Сохранение истории в SQLite.
* Поддержка работы через прокси.

## 🚀 Запуск проекта

Перед запуском создайте файл `.env` в корне проекта:
`BOT_TOKEN=ваш_токен_бота`
`BOT_PROXY=http://user:pass@ip:port`

```bash
# Вариант 1: Запуск через Docker
docker build -t water-bot .
docker run -d --name water-tracker-bot --env-file .env water-bot

# Вариант 2: Локальный запуск
python -m venv venv
source venv/bin/activate  # Для Linux/macOS (или venv\Scripts\activate для Windows)
pip install -r requirements.txt
python bot.py