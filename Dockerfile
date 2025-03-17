# Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Установка необходимых зависимостей
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Установка Python-библиотек
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование файлов приложения
COPY app.py .
COPY templates/ templates/
COPY static/ static/

# Создание директории для временных файлов
RUN mkdir -p uploads

# Открытие порта
EXPOSE 5000

# Запуск приложения
CMD ["python", "app.py"]