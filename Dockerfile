# Лёгкий базовый образ с готовыми колёсами sklearn
FROM python:3.11-slim

# Не буферизуем вывод и не создаём .pyc
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Системные зависимости, которые иногда нужны для pandas/numpy (минимум)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Скопируем только манифест зависимостей (ускоряет билды)
COPY requirements.txt ./requirements.txt

# Убедись, что есть fastapi/uvicorn в requirements.txt (см. ниже)
RUN pip install --no-cache-dir -r requirements.txt

# Код API
COPY app ./app

# По умолчанию модель читаем из /app/models/credit_default_model.pkl
ENV MODEL_PATH=/app/models/credit_default_model.pkl

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]