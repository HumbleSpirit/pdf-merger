#!/bin/bash

# Скрипт для автоматизации сборки и запуска Docker-контейнера

echo "Начинаем сборку Docker-образа pdf-merger..."
docker build -t pdf-merger .

echo "Запускаем контейнер pdf-merger..."
docker run -d --name pdf-merger -p 5000:5000 pdf-merger

echo "PDF Merger запущен и доступен по адресу: http://localhost:5000"