FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY backend/ ./backend/

RUN mkdir -p /app/data /app/logs

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]