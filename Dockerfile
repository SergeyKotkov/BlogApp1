FROM python:3.11-slim

# Установка зависимостей для PostgreSQL и pg_isready
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Сборка статики
RUN python manage.py collectstatic --noinput

# Запуск приложения
CMD ["sh", "-c", "until pg_isready -h $DB_HOST -p $DB_PORT -U $POSTGRES_USER -d $POSTGRES_DB; do echo 'Waiting for PostgreSQL...'; sleep 1; done && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]