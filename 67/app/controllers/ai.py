import datetime
import logging
import time

import numpy as np
import talib

from app.models.candle import factory_candle_class
from app.models.dfcandle import DataFrameCandle
from app.models.events import SignalEvents
from bitflyer.bitflyer import APIClient
from bitflyer.bitflyer import Order
from tradingalgo.algo import ichimoku_cloud

import constants
import settings
import ccxt

logger = logging.getLogger(__name__)


def duration_seconds(duration: str) -> int:
    if duration == constants.DURATION_5S:
        return 5
    if duration == constants.DURATION_1M:
        return 60
    if duration == constants.DURATION_1H:
        return 60 * 60
    else:
        return 0


class AI(object):

    def __init__(self, product_code, use_percent, duration, past_period, stop_limit_percent, back_test):

        if back_test:
            self.signal_events = SignalEvents()
        else:
            self.signal_events = SignalEvents.get_signal_events_by_count(1)

        # pyfxtradingの場合
        # if back_test:
        #     self.signal_events = SignalEvents()
        # else:
        #     self.signal_events = SignalEvents.get_signal_events_by_count(1)
        # pyfxtradingの場合

        self.product_code = product_code
        self.use_percent = use_percent
        self.duration = duration
        self.past_period = past_period
        self.optimized_trade_params = None
        self.stop_limit = 0
        self.stop_limit_percent = stop_limit_percent
        self.back_test = settings.back_test
        self.start_trade = datetime.datetime.utcnow()
        self.candle_cls = factory_candle_class(self.product_code, self.duration)
        self.update_optimize_params(False)

    def update_optimize_params(self, is_continue: bool):
        logger.info('action=update_optimize_params status=run')
        df = DataFrameCandle(self.product_code, self.duration)
        df.set_all_candles(self.past_period)
        if df.candles:
            self.optimized_trade_params = df.optimize_params()
        if self.optimized_trade_params is not None:
            logger.info(f'action=update_optimize_params params={self.optimized_trade_params.__dict__}')

        if is_continue and self.optimized_trade_params is None:
            time.sleep(10 * duration_seconds(self.duration))
            self.update_optimize_params(is_continue)

    def buy(self, candle):

        bitflyer = APIClient(settings.apiKey, settings.secret)
        if self.back_test:

            # pyfxtradingの場合(コメントアウトの理由として、トレードの頻度が増え、シグナルが出やすいストラテジーになるため)
            # if not self.signal_events.can_buy(candle.time):
            #     logger.warning('action=buy status=false error=previous_was_buy')
            #     return False
            # pyfxtradingの場合

            print("back_test is true")
            could_buy = self.signal_events.buy(self.product_code, candle.time, candle.close, amount=1, save= True)
            return could_buy

        else:

            # pyfxtradingの場合
            # if self.start_trade > candle.time:
            #     logger.warning('action=buy status=false error=old_time')
            #     return False
            # pyfxtradingの場合

            # pyfxtradingの場合(コメントアウトの理由として、トレードの頻度が増え、シグナルが出やすいストラテジーになるため)
            # if not self.signal_events.can_buy(candle.time):
            #     logger.warning('action=buy status=false error=previous_was_buy')
            #     return False
            # pyfxtradingの場合

            # pyfxtradingの場合(注文数量の設定を未設定のままにしている、ここで注文数量などを自動化可能)
                # balance = bitflyer.get_balance()
                # avairable_free = balance.available['free']
                # amount = int(avairable_free * self.use_percent)
            # pyfxtradingの場合

            order_data= Order(
                symbol = settings.symbol,
                type= 'limit',
                side= constants.BUY,
                amount= '0.01',
                price= '5007590',
                params = { "product_code" :  settings.product_code}
            )

            symbol = order_data.symbol
            type=order_data.type
            side=order_data.side
            price= order_data.price
            amount=order_data.amount
            params = { "product_code" : settings.product_code}

            # pyfxtradingの場合 (自動化を進める際に必要なコードを記述する)
            # balance = self.API.get_balance()
            # amount = int(balance.available * self.use_percent)
            # order = Order(self.product_code, constants.BUY, amount)
            # pyfxtradingの場合

            bitflyer.send_order(symbol, type, side, amount, price, params)
            print("buy_event")

            could_buy = self.signal_events.buy(self.product_code, candle.time, candle.close, amount=1, save=True)
            print("could_buy")
            return could_buy

    def sell(self, candle):

        bitflyer = APIClient(settings.apiKey, settings.secret)

        if self.back_test:

            # pyfxtradingの場合(コメントアウトの理由として、トレードの頻度が増え、シグナルが出やすいストラテジーになるため)
            # if not self.signal_events.can_sell(candle.time):
            #     logger.warning('action=sell status=false error=previous_was_sell')
            #     return False
            # pyfxtradingの場合

            print("back_test is true")
            could_sell = self.signal_events.sell(self.product_code, candle.time, candle.close, amount=1, save=True)
            return could_sell

        else:
 
            # pyfxtradingの場合
            # if self.start_trade > candle.time:
            #     logger.warning('action=sell status=false error=old_time')
            #     return False
            # pyfxtradingの場合

            # pyfxtradingの場合(コメントアウトの理由として、トレードの頻度が増え、シグナルが出やすいストラテジーになるため)
            # if not self.signal_events.can_sell(candle.time):
            #     logger.warning('action=sell status=false error=previous_was_sell')
            #     return False
            # pyfxtradingの場合(コメントアウトの理由として、トレードの頻度が増え、シグナルが出やすいストラテジーになるため)

            # pyfxtradingの場合(ここでは、sellの決済注文を実行しており、数量を自動化している)
            # trades = self.API.get_open_trade()
            # sum_price = 0
            # amount = 0
            # for trade in trades:
            #     closed_trade = self.API.trade_close(trade.trade_id)
            #     sum_price += closed_trade.price * abs(closed_trade.amount)
            #     amount += abs(closed_trade.amount)
            # pyfxtradingの場合

            order_data= Order(
                symbol = settings.symbol,
                type= 'limit',
                side= constants.SELL,
                amount= '0.01',
                price= '5407590',
                params = { "product_code" :  settings.product_code}
            )

            symbol = order_data.symbol
            type=order_data.type
            side=order_data.side
            price= order_data.price
            amount=order_data.amount
            params = order_data.params

            bitflyer.send_order(symbol, type, side, amount, price, params)
            print("sell_event")

            could_sell = self.signal_events.sell(self.product_code, candle.time, candle.close, amount=1, save=True)
            print("could_sell")
            return could_sell

    def trade(self):
        print("dddddd")
        logger.info('action=trade status=run')
        params = self.optimized_trade_params
        if params is None:
            return

        df = DataFrameCandle(self.product_code, self.duration)
        df.set_all_candles(self.past_period)

        if params.ema_enable:
            ema_values_1 = talib.EMA(np.array(df.closes), params.ema_period_1)
            ema_values_2 = talib.EMA(np.array(df.closes), params.ema_period_2)

        if params.bb_enable:
            bb_up, _, bb_down = talib.BBANDS(np.array(df.closes), params.bb_n, params.bb_k, params.bb_k, 0)

        if params.ichimoku_enable:
            tenkan, kijun, senkou_a, senkou_b, chikou = ichimoku_cloud(df.closes)

        if params.rsi_enable:
            rsi_values = talib.RSI(np.array(df.closes), params.rsi_period)

        if params.macd_enable:
            macd, macd_signal, _ = talib.MACD(np.array(df.closes), params.macd_fast_period, params.macd_slow_period, params.macd_signal_period)

        for i in range(1, len(df.candles)):
            buy_point, sell_point = 0, 0

            if params.ema_enable and params.ema_period_1 <= i and params.ema_period_2 <= i:
                if ema_values_1[i - 1] < ema_values_2[i - 1] and ema_values_1[i] >= ema_values_2[i]:
                    buy_point += 1

                if ema_values_1[i - 1] > ema_values_2[i - 1] and ema_values_1[i] <= ema_values_2[i]:
                    sell_point += 1

            if params.bb_enable and params.bb_n <= i:
                if bb_down[i - 1] > df.candles[i - 1].close and bb_down[i] <= df.candles[i].close:
                    buy_point += 1

                if bb_up[i - 1] < df.candles[i - 1].close and bb_up[i] >= df.candles[i].close:
                    sell_point += 1

            if params.ichimoku_enable:
                if (chikou[i-1] < df.candles[i-1].high and
                        chikou[i] >= df.candles[i].high and
                        senkou_a[i] < df.candles[i].low and
                        senkou_b[i] < df.candles[i].low and
                        tenkan[i] > kijun[i]):
                    buy_point += 1

                if (chikou[i - 1] > df.candles[i - 1].low and
                        chikou[i] <= df.candles[i].low and
                        senkou_a[i] > df.candles[i].high and
                        senkou_b[i] > df.candles[i].high and
                        tenkan[i] < kijun[i]):
                    sell_point += 1

            if params.macd_enable:
                if macd[i] < 0 and macd_signal[i] < 0 and macd[i - 1] < macd_signal[i - 1] and macd[i] >= macd_signal[i]:
                    buy_point += 1

                if macd[i] > 0 and macd_signal[i] > 0 and macd[i-1] > macd_signal[i - 1] and macd[i] <= macd_signal[i]:
                    sell_point += 1

            if params.rsi_enable and rsi_values[i-1] != 0 and rsi_values[i-1] != 100:
                if rsi_values[i-1] < params.rsi_buy_thread and rsi_values[i] >= params.rsi_buy_thread:
                    buy_point += 1

                if rsi_values[i-1] > params.rsi_sell_thread and rsi_values[i] <= params.rsi_sell_thread:
                    sell_point += 1

            if buy_point > 0:
                if not self.buy(df.candles[i]):
                    continue

                self.stop_limit = df.candles[i].close * self.stop_limit_percent

            if sell_point > 0 or self.stop_limit > df.candles[i].close:
                if not self.sell(df.candles[i]):
                    continue

                self.stop_limit = 0.0
                self.update_optimize_params(is_continue=True)