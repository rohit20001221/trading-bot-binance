from redis_om import JsonModel
from config import redis

class OHLC(JsonModel):
    symbol : str
    open: float
    high: float
    low: float
    close: float
    volume: float

    class Meta:
        database = redis