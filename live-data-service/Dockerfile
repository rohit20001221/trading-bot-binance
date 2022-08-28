FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY live-data-service/requirements.txt .

RUN pip install -r requirements.txt

COPY live-data-service .

COPY protobufs /protobufs

RUN python -m grpc_tools.protoc -I /protobufs --python_out=/app --grpc_python_out=/app /protobufs/historical-data.proto

CMD [ "python", "ws.py" ]