from redis_om import HashModel, Field
from config import redis

class OHLC(HashModel):
    symbol : str = Field(index=True)
    open: float
    high: float
    low: float
    close: float
    volume: float

    class Meta:
        database = redis