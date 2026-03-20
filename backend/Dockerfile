# Fly.io / container deploy for FastAPI contact API
FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Fly sets PORT; default 8080 matches fly.toml internal_port
ENV PORT=8080
EXPOSE 8080

# Shell form so Fly's $PORT is applied at container start
CMD sh -c "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}"
