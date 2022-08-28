from typing import List
from entities.strategy import Strategy
from strategies.ema import EMAStrategy
import threading
import os

API_KEY = os.environ['API_KEY']
API_SECRET = os.environ['API_SECRET']

channel_name = os.environ['CHANNEL_NAME']

strategies : List[Strategy] = [
    EMAStrategy(API_KEY, API_SECRET, channel_name)
]

threads : List[threading.Thread] = []

for strategy in strategies:
    thread = threading.Thread(
        target=strategy.start,
    )

    thread.run()

for thread in threads:
    thread.join()