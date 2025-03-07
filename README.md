# REST API. Тестовое задание на вакансию Python Backend Developer

## Быстрый способ запустить приложение
1. Скопируйте репозиторий:
    ```
    git clone https://github.com/artkzmin/dimatech
    ```
2. Переименуйте файл `.env.dist` на `.env`.
3. Из корня проекта выполните команду Docker Compose:
    ```
    docker-compose up -d
    ```
    Запуск контейнера с API отложен на 30 секунд, поэтому потребуется подождать.
4. Документация API будет доступна по адресу: http://127.0.0.1:8000/docs; само API - http://127.0.0.1:8000/.

## Тестовые данные по умолчанию (из файла `.env.dist`)
### Администратор
Email - `admin@domain.com`

Password - `Fuo5|%2bwAc?bGl|j9|C`

Вы также можете указать собственные данные в файле `.env`:
```
ADMIN_EMAIL=admin@domain.com
ADMIN_PASSWORD="Fuo5|%2bwAc?bGl|j9|C"
ADMIN_NAME=Брэд
ADMIN_SURNAME=Питт
ADMIN_PATRONYMIC=Иванович
```
### Обычный пользователь
Email - `common@domain.com`

Password - `s{pRbpe82bndKqnb2q7~`

Вы также можете указать собственные данные в файле `.env`:
```
COMMON_EMAIL=common@domain.com
COMMON_PASSWORD="spRbpe82bndKqnb2q7~"
COMMON_NAME=Роберт
COMMON_SURNAME=Дауни
COMMON_PATRONYMIC=Младший
```
### Счет
id - `1`

user_id - `1`

balance - `0`

## Запуск приложения

### Переменные окружения
Разместите файл с переменными окружения `.env` в корне проекта. Пример файла `.env` - `.env.dist` (заполнен тестовыми данными).
### Способ №1. Docker Compose
**Обязательно** укажите в файле `.env` следующие данные для хоста и порта БД (они указаны также в файле `.env.dist`), остальные данные могут быть собственные:
```
DB_HOST=dimatech_db
DB_PORT=5432
```
Запуск Docker Compose:
```
docker-compose up -d
```
Запуск контейнера с API отложен на 30 секунд, поэтому потребуется подождать.

### Способ №2. Запуск Python-скрипта
#### Переменный окружения
Укажите в файле `.env` данные для подключения к вашей базе данных PostgreSQL:
```
DB_HOST=...
DB_PORT=...
```
#### Запуск приложения
Из корня проекта выполните команды:
1. Для Linus/MacOS:

    Создание виртуального окружения:
    ```
    python3 -m venv venv
    ```
    Активация виртуального окружения:
    ```
    source venv/bin/activate
    ```
    Установка зависимостей:
    ```
    pip install -r requirements.txt
    ```
    Миграции в базу данных:
    ```
    alembic upgrade head
    ```
    Создание тестовых данных:
    ```
    python src/init.py
    ```
    Запуск приложения:
    ```
    python src/main.py
    ```
2. Для Windows:

    Создание виртуального окружения:
    ```
    python -m venv venv
    ```
    Активация виртуального окружения:
    ```
    .\venv\Scripts\activate.bat
    ```
    Установка зависимостей:
    ```
    pip install -r requirements.txt
    ```
    Миграции в базу данных:
    ```
    alembic upgrade head
    ```
    Создание тестовых данных:
    ```
    python .\src\init.py
    ```
    Запуск приложения:
    ```
    python .\src\main.py
    ```

Документация API будет доступна по адресу: http://127.0.0.1:8000/docs, само API - http://127.0.0.1:8000/. Если вы меняли порт в `.env`, используйте собственный порт вместо `8000`.

## Стек приложения

1. PostgreSQL
2. SQLAlchemy
3. FastAPI
4. Docker Compose
5. Alembic
6. Ruff
7. Pytest
