from entities.strategy import Strategy
from talib.abstract import EMA, SMA
import numpy as np
from binance.enums import ORDER_TYPE_MARKET, SIDE_BUY, SIDE_SELL
from collections import defaultdict
import os

# In[2]:

API_KEY=os.environ['API_KEY']
API_SECRET=os.environ['API_SECRET']


class EMAStrategy(Strategy):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.balance : float = float(self.client.get_asset_balance('usdt')['free'])
        self.risk_per_trade_percentage = 0.01
        self.stop_loss_percentage = 0.01

        self.current_stop_loss = 0
        self.positions = defaultdict(float)

        self.stop_loss_hit_count = 0

    def calculate_position_sizing_and_stop_loss(self, current_price):
        loss_amount = self.balance * self.risk_per_trade_percentage
        stop_loss = (1 - self.stop_loss_percentage) * current_price

        return loss_amount / stop_loss, stop_loss

    def update_stop_loss_hit_count(self):
        self.stop_loss_hit_count += 1

        if self.stop_loss_hit_count >= 2:
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

        print(latest_ema200, latest_ema150, is_close_ema, ema_gradient, latest_volume, latest_volume_average)

        if is_close_ema:
            if ema_gradient > 0 and latest_ema150 > latest_ema200 and latest_volume > latest_volume_average:
                quantity, stop_loss = self.calculate_position_sizing_and_stop_loss(live['close'])

                self.notify(
                    "entry signal",
                    f"{latest_ema200}, {latest_ema150}, {is_close_ema}, {ema_gradient}, {latest_volume}, {latest_volume_average}"
                )

                try:
                    self.client.create_order(
                        symbol=live['symbol'],
                        type=ORDER_TYPE_MARKET,
                        side=SIDE_BUY,
                        quantity=quantity
                    )

                    self.current_stop_loss = stop_loss
                    self.positions[live['symbol']] += quantity

                    self.notify(
                        "order placed",
                        f"ENTRY:- {quantity} {live['close']} {stop_loss}"
                    )
                except:
                    self.current_stop_loss = 0

    def handle_live_data(self, live):
        if live['close'] <= self.current_stop_loss and self.positions[live['symbol']] > 0:
            # exit the trade
            quantity = self.positions[live['symbol']]

            self.update_stop_loss_hit_count()
            try:
                self.client.create_order(
                    symbol=live['symbol'],
                    type=ORDER_TYPE_MARKET,
                    side=SIDE_SELL,
                    quantity=quantity
                )
            except:
                return
            finally:
                self.positions.pop(live['symbol'])
                self.current_stop_loss = 0

                self.notify(
                    "order placed",
                    f"EXIT:- {quantity} {live['close']} REASON:- Stop Loss"
                )

ema = EMAStrategy(API_KEY, API_SECRET, os.environ['CHANNEL_NAME'], True)
ema.start()