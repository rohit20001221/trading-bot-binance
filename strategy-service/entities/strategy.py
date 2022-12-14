import json
from binance.client import Client
from redis_om import get_redis_connection
import numpy as np
import grpc
from portfolio_pb2_grpc import PortfolioServiceStub
from pushbullet import API
import os

class Strategy:
    def __init__(self, api_key: str, api_secret: str, name: str, redis_host='redis_server', redis_port=6379) -> None:
        self.client : Client = Client(api_key, api_secret)

        self.redis = get_redis_connection(
            host=redis_host,
            port=redis_port,
            decode_responses=True
        )
        self.name = name

        self.pubsub = self.redis.pubsub()
        self.pubsub.subscribe(self.name)

        self.portfolio_grpc_channel = grpc.insecure_channel("portfolio:50051")
        self.portfolio_client = PortfolioServiceStub(self.portfolio_grpc_channel)

        self.notifier = API()
        self.notifier.set_token(os.environ['PUSHBULLET_ACCESS_TOKEN'])

    def handle_kline_data(self, klines, live):
        raise NotImplementedError("not impleted handle_live_data")

    def handle_live_data(self, live):
        raise NotImplementedError("not implemented handle_kline_data")

    def start(self):
        for message in self.pubsub.listen():
            if message["type"] == "message":
                data = json.loads(message["data"])

                if data["is_interval"]:
                    candles = self.client.get_klines(symbol=data["symbol"], interval=data["interval"], limit=1000)
                    klines = list(map(lambda x : [float(x[1]), float(x[2]), float(x[3]), float(x[4]), float(x[5])], candles))
                    klines = np.array(klines)

                    self.handle_kline_data(klines, data)
                else:
                    self.handle_live_data(data)