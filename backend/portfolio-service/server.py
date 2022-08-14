from concurrent import futures
from config import redis
import grpc

from portfolio_pb2 import (
    OrderResponse,
    Position,
    ClearPositionResponse,
    StopLossHitResponse,
)

from models import OrderModel

import portfolio_pb2_grpc

class PortfolioService(portfolio_pb2_grpc.PortfolioServiceServicer):
    def GetPosition(self, request, context):
        quantity = redis.get(request.symbol)

        if quantity == None:
            _position = Position(
                symbol=request.symbol,
                quantity=0
            )

            redis.set(request.symbol, 0)
        else:
            _position = Position(
                symbol=request.symbol,
                quantity=float(quantity)
            )

        return _position

    def UpdatePosition(self, request, context):
        _position_quantity = redis.get(request.symbol)

        if _position_quantity == None:
            redis.set(request.symbol, request.quantity)
        else:
            redis.set(request.symbol, request.quantity + float(_position_quantity))

        updated_position_quantity = redis.get(request.symbol)
        return Position(
            symbol=request.symbol,
            quantity=float(updated_position_quantity)
        )

    def CreateOrder(self, request, context):
        order = OrderModel(
            symbol=request.symbol,
            type=request.type,
            side=request.side,
            quantity=request.quantity,
            stoploss=request.stoploss,
            channel_name=request.channel_name
        )
        order.save()

        return OrderResponse(pk=order.pk)

    def ClearPosition(self, request, context):
        redis.delete(request.symbol)

        return ClearPositionResponse(status=True)

    def GetStopLossHitCount(self, request, context):
        stop_loss_hit_count = redis.get("stop_loss_hit_count")

        if stop_loss_hit_count == None:
            stop_loss_hit_count = 0
            redis.set("stop_loss_hit_count", 0)

        return StopLossHitResponse(stop_loss_hit_count=stop_loss_hit_count)

    def IncrementStopLoss(self, request, context):
        stop_loss_hit_count = redis.get("stop_loss_hit_count")

        if stop_loss_hit_count == None:
            stop_loss_hit_count = 0
        else:
            stop_loss_hit_count = int(stop_loss_hit_count)

        redis.set("stop_loss_hit_count", stop_loss_hit_count + 1)

        stop_loss_hit_count = int(redis.get("stop_loss_hit_count"))
        return StopLossHitResponse(stop_loss_hit_count=stop_loss_hit_count)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    portfolio_pb2_grpc.add_PortfolioServiceServicer_to_server(
        PortfolioService(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()