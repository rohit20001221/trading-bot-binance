FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED 1

RUN apt-get update

RUN apt-get install -y wget tar gcc build-essential

RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz

RUN tar -xzf ta-lib-0.4.0-src.tar.gz

WORKDIR /ta-lib

RUN ./configure

RUN make

RUN make install

RUN pip install ta-lib

ENV LD_LIBRARY_PATH /usr/local/lib:$LD_LIBRARY_PATH

WORKDIR /app

COPY strategy-service .

RUN pip install -r requirements.txt

COPY protobufs /protobufs

RUN python -m grpc_tools.protoc -I /protobufs --python_out=/app --grpc_python_out=/app /protobufs/portfolio.proto

CMD [ "python", "init.py" ]