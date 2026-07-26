FROM python:3.11-slim

# Отключаем создание .pyc файлов и включаем мгновенный вывод логов в консоль
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы проекта
COPY . .

CMD ["python", "bot.py"]