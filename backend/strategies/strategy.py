import json
from binance.client import Client
import redis
import numpy as np
import subprocess

class Strategy:
    def __init__(self, api_key: str, api_secret: str, name: str, redis_host='127.0.0.1', redis_port=6379) -> None:
        self.test_client : Client = Client(api_key, api_secret, testnet=True)
        self.client : Client = Client(api_key, api_secret)

        self.redis = redis.Redis(
            host=redis_host,
            port=redis_port,
            decode_responses=True
        )
        self.name = name

        self.pubsub = self.redis.pubsub()
        self.pubsub.subscribe(self.name)

    def handle_kline_data(self, klines, live):
        raise NotImplementedError("not impleted handle_live_data")

    def handle_live_data(self, live):
        raise NotImplementedError("not implemented handle_kline_data")

    def notify(self, title, message):
        subprocess.call(["notify-send", title, message])

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