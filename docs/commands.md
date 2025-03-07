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

## Транзакции
### Генерация ключа
```
62a8ab5248da1290326e3113fe6b6f6f1ad2e78f5022fac5cb573207281c2f9d
```