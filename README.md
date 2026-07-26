# 💧 Water Tracker Telegram Bot

Асинхронный Telegram-бот для расчета индивидуальной нормы воды и трекинга ежедневного водного баланса.

---

## 🛠 Технологический стек

* **Python 3.11+**
* **aiogram 3.x** - асинхронный фреймворк для Telegram Bot API (FSM, Routers, Keyboards)
* **SQLAlchemy 2.0 (AsyncORM) + aiosqlite** - асинхронная работа с базой данных SQLite
* **Pydantic v2** - строгая валидация и обработка пользовательского ввода
* **Docker** - контейнеризация проекта для быстрого и надежного деплоя
* **python-dotenv** - управление конфигурацией и секретами через файл `.env`

---

## ⚙️ Функционал

* Расчет индивидуальной суточной нормы воды на основе веса пользователя.
* Быстрое добавление выпитого объема через удобные интерфейсные кнопки.
* Наглядный прогресс-бар выпитой воды за текущий день.
* Сохранение истории и данных пользователей в SQLite.
* Поддержка работы через прокси.

---

## 🚀 Быстрый запуск

### 1. Подготовка конфигурации

Перед запуском в любом окружении создайте файл `.env` в корне проекта:

```env
BOT_TOKEN=ваш_токен_от_BotFather
BOT_PROXY=http://user:pass@ip:port  # Необязательно, если нужен прокси

```

---

### 🌐 Развертывание на VPS (Ubuntu 22.04 / Debian)

1. **Установите Git и Docker на сервер:**
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y git docker.io
sudo systemctl enable --now docker

```


2. **(Опционально) Добавьте пользователя в группу Docker:**
```bash
sudo usermod -aG docker $USER
newgrp docker

```


3. **Клонируйте репозиторий и перейдите в папку:**
```bash
git clone [https://github.com/serotoninR/water-tracker-telegram-bot.git](https://github.com/serotoninR/water-tracker-telegram-bot.git)
cd water-tracker-telegram-bot

```


4. **Создайте файл `.env`:**
```bash
nano .env

```


*Вставьте переменные окружения, нажмите `Ctrl + O`, `Enter` для сохранения и `Ctrl + X` для выхода.*
5. **Соберите и запустите Docker-контейнер:**
```bash
docker build -t water-bot .
docker run -d \
  --name water-tracker-bot \
  --restart unless-stopped \
  --env-file .env \
  water-bot

```


*Флаг `--restart unless-stopped` обеспечивает автоматический перезапуск бота при перезагрузке сервера или сбоях.*

---

### 💻 Локальный запуск через Docker

```bash
# Сборка образа
docker build -t water-bot .

# Запуск контейнера
docker run -d --name water-tracker-bot --env-file .env water-bot

```

---

### 🐍 Локальный запуск без Docker (Python)

```bash
# Создание виртуального окружения
python -m venv venv

# Активация:
# Для Linux/macOS:
source venv/bin/activate
# Для Windows (PowerShell):
# .\venv\Scripts\Activate.ps1

# Установка зависимостей и запуск
pip install -r requirements.txt
python bot.py

```

---

## 📊 Полезные команды для управления (Docker)

* **Просмотр логов в реальном времени:**
```bash
docker logs -f water-tracker-bot

```


* **Проверить статус контейнера:**
```bash
docker ps

```


* **Перезапустить бота:**
```bash
docker restart water-tracker-bot

```


* **Остановить и удалить контейнер:**
```bash
docker stop water-tracker-bot
docker rm water-tracker-bot

```