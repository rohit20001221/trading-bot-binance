import asyncio
import websockets
import json
from config import redis
import os
import grpc

from historical_data_pb2_grpc import HistoricalDataServiceStub
from historical_data_pb2 import (
    AddOHLCRequest,
    ClearHistoricalDataRequest,
    OHLC,
    GetHistoricalDataRequest
)

socket_address = 'wss://stream.binance.com:9443'
symbol = os.environ['SYMBOL']
interval = os.environ['INTERVAL']

binance_endpoint = socket_address + '/ws/' + symbol + '@' + 'kline_' + interval

channels = [
    os.environ['CHANNEL_NAME'],
]

async def get_live_data():
    async with websockets.connect(binance_endpoint) as websocket:
        historical_data_grpc_channel = grpc.insecure_channel('historical-data:50051')
        historical_data_client = HistoricalDataServiceStub(historical_data_grpc_channel)

        # clear the historical data
        historical_data_client.ClearHistoricalData(
            ClearHistoricalDataRequest(
                symbol=symbol
            )
        )

        # fetch the historical data from the api and store it in the database

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

            if x:
                historical_data_client.AddOHLC(
                    AddOHLCRequest(
                        ohlc = OHLC(
                            open=o,
                            high=h,
                            low=l,
                            close=c,
                            volume=v
                        ),
                        symbol=symbol,
                    )
                )

                _data = historical_data_client.GetHistoricalData(
                    GetHistoricalDataRequest(
                        symbol=symbol
                    )
                )
                print(_data)

            for channel in channels:
                redis.publish(channel, data)

asyncio.run(get_live_data())