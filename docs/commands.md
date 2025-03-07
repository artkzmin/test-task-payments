# Полезные команды для разработки

## Alembic
### Инициализация
```
alembic init src/migrations
```
После инициализации необходимо отредактировать `alembic.ini` и `src/migrations/env.py` под проект.
```
### Создание ревизии
```
alembic revision --autogenerate -m "comment"
```
### Применение миграций
```
alembic upgrade head
```
