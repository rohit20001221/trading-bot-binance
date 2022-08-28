from redis_om import HashModel
from config import redis

class OrderModel(HashModel):
    symbol: str
    type: str
    side: str
    quantity: float
    stoploss: float
    channel_name: str

    class Meta:
        database = redis