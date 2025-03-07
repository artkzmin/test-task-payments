FROM python:3.11.9

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

COPY .env .env

# Запуск отложен, чтобы успел развернуться контейнер с базой данных
CMD sleep 30; alembic upgrade head; python src/init.py; python src/main.py