FROM python:3.11-slim

# Установка системных зависимостей для сборки psycopg2 и Pillow
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Настройка рабочей директории
WORKDIR /app

# Отключаем буферизацию вывода и запись pyc файлов
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Копирование и установка зависимостей
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копирование всего исходного кода
COPY . /app/

# Создание директорий для статических и медиа файлов
RUN mkdir -p /app/static /app/media

# Запуск приложения через WSGI-сервер Gunicorn на порту 8000
CMD ["gunicorn", "shop.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]