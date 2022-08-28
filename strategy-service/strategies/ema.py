from entities.strategy import Strategy
from talib.abstract import EMA, SMA
import numpy as np
from binance.enums import ORDER_TYPE_MARKET, SIDE_BUY, SIDE_SELL
import os
from portfolio_pb2 import (
    Position, GetPositionRequest, OrderRequest, ClearPositionRequest, StopLossHitCountRequest, IncrementStopLossHitRequest
)

class EMAStrategy(Strategy):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.balance : float = float(self.client.get_asset_balance('usdt')['free'])
        self.risk_per_trade_percentage = 0.01
        self.stop_loss_percentage = 0.01

        self.current_stop_loss = 0
        self.stop_loss_hit_count = 0

    def calculate_position_sizing_and_stop_loss(self, current_price):
        loss_amount = self.balance * self.risk_per_trade_percentage
        stop_loss = (1 - self.stop_loss_percentage) * current_price

        return loss_amount / stop_loss, stop_loss

    def update_stop_loss_hit_count(self):
        self.portfolio_client.IncrementStopLoss(IncrementStopLossHitRequest())

        if self.portfolio_client.GetStopLossHitCount(StopLossHitCountRequest()) >= 2:
            print('[**] Max Loss Reached')
            exit(0)

    def handle_kline_data(self, klines, live):
        ema200 = EMA(klines[:,3], 200)
        ema150 = EMA(klines[:,3], 150)
        sma_volume = SMA(klines[:,4], 20)

        is_close_ema = np.isclose(ema150, ema200)[-1]
        ema_gradient = np.gradient(ema150-ema200)[-1]

        latest_volume = live['volume']
        latest_volume_average = sma_volume[-1]

        latest_ema200 = ema200[-1]
        latest_ema150 = ema150[-1]

        if is_close_ema:
            if ema_gradient > 0 and latest_ema150 > latest_ema200 and latest_volume > latest_volume_average:
                quantity, stop_loss = self.calculate_position_sizing_and_stop_loss(live['close'])

                try:
                    self.notifier.send_note(
                        "Entry Signal", live["symbol"]
                    )

                    self.current_stop_loss = stop_loss

                    self.portfolio_client.UpdatePosition(
                        Position(symbol=live['symbol'], quantity=quantity)
                    )
                    self.portfolio_client.CreateOrder(
                        OrderRequest(
                            symbol=live["symbol"],
                            quantity=quantity,
                            side=SIDE_BUY,
                            stoploss=stop_loss,
                            type=ORDER_TYPE_MARKET
                        )
                    )
                except:
                    self.current_stop_loss = 0

    def handle_live_data(self, live):
        position = self.portfolio_client.GetPosition(GetPositionRequest(symbol=live["symbol"]))

        if live['close'] <= self.current_stop_loss and position.quantity > 0:
            try:
                self.notifier.send_note("Stop Loss", live["symbol"])
            except:
                pass

            # exit the trade
            quantity = position.quantity

            self.update_stop_loss_hit_count()
            self.portfolio_client.CreateOrder(
            OrderRequest(
                    symbol=live["symbol"],
                    quantity=quantity,
                    side=SIDE_SELL,
                    type=ORDER_TYPE_MARKET
                )
            )

            self.portfolio_client.ClearPosition(ClearPositionRequest(symbol=live["symbol"]))
            self.current_stop_loss = 0

if __name__ == '__main__':
    API_KEY=os.environ['API_KEY']
    API_SECRET=os.environ['API_SECRET']

    ema = EMAStrategy(API_KEY, API_SECRET, os.environ['CHANNEL_NAME'], True)
    ema.start()