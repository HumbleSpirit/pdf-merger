# PDF Merger

Простой веб-сервис для загрузки, упорядочивания и объединения PDF-файлов.

## Особенности

- Загрузка нескольких PDF-файлов
- Интерактивное изменение порядка файлов перетаскиванием
- Объединение PDF-файлов в один документ
- Простое развертывание с помощью Docker

## Требования

- Docker

## Быстрый старт

### Вариант 1: С помощью Docker Run

```bash
# Сборка образа
docker build -t pdf-merger .

# Запуск контейнера
docker run -d --name pdf-merger -p 5000:5000 pdf-merger
```

### Вариант 2: С помощью скрипта (Linux/Mac)

```bash
chmod +x build_and_run.sh
./build_and_run.sh
```

### Вариант 3: С помощью скрипта (Windows)

```
build_and_run.bat
```

### Вариант 4: С помощью Docker Compose

```bash
docker-compose up -d
```

## Использование

1. Откройте веб-браузер и перейдите по адресу: http://localhost:5000
2. Загрузите PDF-файлы для объединения
3. Перетащите файлы, чтобы изменить порядок объединения
4. Нажмите "Объединить PDF" и сохраните результат

## Ограничения

- Максимальный размер файла: 16 МБ (можно изменить в настройках)
- Поддерживаются только PDF-файлы