from concurrent import futures
import grpc

from historical_data_pb2 import (
    AddOHLCResponse,
    ClearHistoricalDataResponse,
    GetHistoricalDataResponse,
)
import historical_data_pb2_grpc
from models import OHLC

class HistoricalDataService(historical_data_pb2_grpc.HistoricalDataServiceServicer):
    def AddOHLC(self, request, context):
        ohlc = OHLC(
            symbol=request.symbol,
            open=request.open,
            high=request.high,
            low=request.low,
            close=request.close,
            volume=request.volume
        )
        ohlc.save()

        return AddOHLCResponse()

    def GetHistoricalData(self, request, context):
        return super().GetHistoricalData(request, context)

    def ClearHistoricalData(self, request, context):
        try: OHLC.find((OHLC.symbol == request.symbol)).delete()
        except: pass

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