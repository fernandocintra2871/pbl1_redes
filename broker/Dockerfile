FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install Flask

CMD ["python", "app/broker.py"]