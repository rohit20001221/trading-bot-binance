FROM python:3.8-slim-buster

WORKDIR /app

COPY portfolio-service .

RUN pip install -r requirements.txt

COPY protobufs /protobufs

RUN python -m grpc_tools.protoc -I /protobufs --python_out=/app --grpc_python_out=/app /protobufs/portfolio.proto

CMD [ "python", "server.py" ]