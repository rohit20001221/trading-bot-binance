from concurrent import futures
import grpc

from historical_data_pb2 import (
    AddOHLCResponse,
    ClearHistoricalDataResponse,
    GetHistoricalDataResponse,
    GetHistoricalDataOHLC
)
import historical_data_pb2_grpc
from config import redis

class HistoricalDataService(historical_data_pb2_grpc.HistoricalDataServiceServicer):
    def AddOHLC(self, request, context):
        ohlc = request.ohlc

        data = {
            "open": ohlc.open,
            "high": ohlc.high,
            "low": ohlc.low,
            "close": ohlc.close,
            "volume": ohlc.volume
        }
        redis.json().arrappend(f"historical-{request.symbol}", "$", data)

        return AddOHLCResponse()

    def GetHistoricalData(self, request, context):
        response = []
        for data in redis.json().get(f"historical-{request.symbol}", "$")[0]:
            response.append(
                GetHistoricalDataOHLC(
                    open=data['open'],
                    high=data['high'],
                    low=data['low'],
                    close=data['close'],
                    volume=data['volume']
                )
            )

        return GetHistoricalDataResponse(data=response)

    def ClearHistoricalData(self, request, context):
        redis.json().set(f"historical-{request.symbol}", "$", [])

        return ClearHistoricalDataResponse()


def server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    historical_data_pb2_grpc.add_HistoricalDataServiceServicer_to_server(
        HistoricalDataService(), server
    )

    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    server()