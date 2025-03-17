# Используем официальный образ Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем необходимые пакеты
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Копируем файлы requirements.txt
COPY requirements.txt .

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Создаем директории для проекта
RUN mkdir -p /app/static /app/templates /app/uploads

# Копируем исходные файлы приложения
COPY app.py /app/
COPY static/styles.css /app/static/
COPY templates/index.html /app/templates/
COPY templates/arrange.html /app/templates/

# Создаем правильные разрешения для загрузок
RUN chmod 777 /app/uploads

# Открываем порт 5000
EXPOSE 5000

# Запускаем приложение при старте контейнера
CMD ["python", "app.py"]