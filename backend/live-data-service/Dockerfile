FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY live-data-service/requirements.txt .

RUN pip install -r requirements.txt

COPY live-data-service .

CMD [ "python", "ws.py" ]