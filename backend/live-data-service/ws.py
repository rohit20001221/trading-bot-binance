import asyncio
import websockets
import json
from redis import Redis
import os

socket_address = 'wss://stream.binance.com:9443'
symbol = os.environ['SYMBOL']
interval = os.environ['INTERVAL']

binance_endpoint = socket_address + '/ws/' + symbol + '@' + 'kline_' + interval

REDIS_HOST = 'redis_server'
REDIS_PORT = 6379
redis = Redis(REDIS_HOST, REDIS_PORT, decode_responses=True)

channels = [
    os.environ['CHANNEL_NAME'],
]

async def get_live_data():
    async with websockets.connect(binance_endpoint) as websocket:
        while True:
            try:
                data = await websocket.recv()
            except:
                exit(0)

            klines = json.loads(data)['k']

            o, h, l, c, x, v = float(klines['o']), float(klines['h']), float(klines['l']), float(klines['c']), klines['x'], float(klines['v'])

            data = json.dumps({
                'open': o, 'high': h, 'low': l, 'close': c,
                'volume': v, 'is_interval': x, "symbol": symbol.upper(), "interval": interval
            })

            for channel in channels:
                redis.publish(channel, data)

asyncio.run(get_live_data())