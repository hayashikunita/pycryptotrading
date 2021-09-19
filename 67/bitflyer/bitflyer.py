from datetime import datetime
import logging
import math
import time
from typing import get_args

import dateutil.parser
import ccxt

import constants
import settings

logger = logging.getLogger(__name__)

class BaseError (Exception):
    pass

class Balance(object):
    def __init__(self, available, collateral):
        self.available = available
        self.collateral = collateral

class Ticker(object):
    def __init__(self, product_code,timestamp, bid, ask, volume):
        self.product_code = product_code
        self.timestamp = timestamp
        self.ask = ask
        self.bid = bid
        self.volume = volume

    @property
    def mid_price(self):
        return (self.bid + self.ask) / 2

    @property
    def time(self):
        return datetime.utcfromtimestamp(self.timestamp)

    def truncate_date_time(self, duration):
        ticker_time = self.time
        if duration == constants.DURATION_5S:
            new_sec = math.floor(self.time.second / 5) * 5
            ticker_time = datetime(
                self.time.year, self.time.month, self.time.day,
                self.time.hour, self.time.minute, new_sec)
            time_format = '%Y-%m-%d %H:%M:%S'
        elif duration == constants.DURATION_1M:
            time_format = '%Y-%m-%d %H:%M'
        elif duration == constants.DURATION_1H:
            time_format = '%Y-%m-%d %H'
        else:
            logger.warning('action=truncate_date_time error=no_datetime_format')
            return None

        str_date = datetime.strftime(ticker_time, time_format)
        return datetime.strptime(str_date, time_format)

class Order(object):
    def __init__(self,symbol,type, side, amount,price,params): 
        self.symbol = symbol
        self.type = type
        self.side= side
        self.price = price
        self.amount = amount
        self.params = params

class TradesSummary(object):
    def __init__(self, id, side, price, amount):
        self.id = id
        self.side = side
        self.price = price
        self.amount = amount

class OrdersSummary(object):
    def __init__(self, side, product_code, amount, order_type, order_state, id):
        self.product_code = product_code
        self.side = side
        self.amount = amount
        self.order_type = order_type
        self.order_state = order_state
        self.id = id

class APIClient(object):
    def __init__(self, apiKey, secret):
        self.apiKey = apiKey
        self.secret = secret 

    def get_balance(self) -> Balance:

        bitflyer = ccxt.bitflyer()
        bitflyer.apiKey = self.apiKey
        bitflyer.secret = self.secret
        balance = bitflyer.fetchBalance()
        getcollateral = bitflyer.private_get_getcollateral()
        collateral = getcollateral["collateral"]
        available = balance["JPY"]
        return Balance(available, collateral)

    def send_order(self, symbol, type, side, amount, price, params):
        bitflyer = ccxt.bitflyer()
        bitflyer.apiKey = self.apiKey
        bitflyer.secret=  self.secret
        order_data= Order(
            symbol = symbol,
            type=type,
            side=side,
            amount=amount,
            price=price,
            params=params
        )
        try:
            order = bitflyer.create_order(order_data.symbol, order_data.type, order_data.side, order_data.amount, order_data.price, order_data.params)
            return order
        except ccxt.BaseError as e:
            print("BitflyerのAPIでエラー発生",e)

        # アルゴリズムにする際、適切な例外処理ではなかった為、一旦コメントアウト
        # while True:
                # try:
                #     order =bitflyer.create_order(order_data.symbol, order_data.type, order_data.side, order_data.amount, order_data.price, order_data.params)
                #     return order
                # except ccxt.BaseError as e:
                #     print("BitflyerのAPIでエラー発生",e)
                #     print("注文の通信が失敗しました。5秒後再度オーダーを出します。")
                #     time.sleep(5)
        # アルゴリズムにする際、適切な例外処理ではなかった為、一旦コメントアウト

    def fetch_open_order(self):
        bitflyer = ccxt.bitflyer()
        bitflyer.apiKey = self.apiKey
        bitflyer.secret=  self.secret
        openorder = bitflyer.fetch_open_orders(settings.product_code)
        return openorder

        # 例外処理で途中まで考えた関数、今後例外処理で使えるかもしれないのでいったんコメントアウト
        # def wait_order_complete(self, count=0, timeout_count=5):
        #     bitflyer = ccxt.bitflyer()
        #     bitflyer.apiKey=self.apiKey
        #     bitflyer.secret=self.secret
        #     while True:
        #         gettrades = bitflyer.fetch_my_trades(
        #                 symbol = settings.symbol,
        #                 params = { "product_code" : settings.product_code}
        #         )
        #         getorders = bitflyer.fetch_orders(
        #             symbol = settings.symbol,
        #             params = { "product_code" : settings.product_code}
        #         )
        #         if gettrades[-1]['info']['child_order_acceptance_id'] != getorders[-1]['info']['child_order_acceptance_id']:
        #             # 約定済みのtradesを取得する。return bitflyer.fetch_my_trades(settings.product_code)
        #             time.sleep(1)
        #             count += 1
        #             if count > timeout_count:
        #                 return None
        #         if gettrades[-1]['info']['child_order_acceptance_id'] == getorders[-1]['info']['child_order_acceptance_id']:
        #                 return gettrades[-1]['info']['child_order_acceptance_id']
        # 例外処理で途中まで考えた関数、今後例外処理で使えるかもしれないのでいったんコメントアウト

    def cancel_new_order(self):
        bitflyer = ccxt.bitflyer()
        bitflyer.apiKey = settings.apiKey
        bitflyer.secret=  settings.secret

        orders = bitflyer.fetch_open_orders(
            symbol = settings.symbol,
            params = { "product_code" : settings.product_code }
        )

        bitflyer.cancel_order(
            symbol = settings.symbol,
            id = orders[-1]["id"], 
            params = { "product_code" : settings.product_code}
        )

    def fetch_all_orders(self):
        bitflyer = ccxt.bitflyer()
        bitflyer.apiKey = self.apiKey
        bitflyer.secret=  self.secret
        orders = bitflyer.fetch_orders(
            symbol = settings.symbol,
            params = { "product_code" : settings.product_code}
        )
        return orders

    def fetch_all_trades(self):
        bitflyer = ccxt.bitflyer()
        bitflyer.apiKey = self.apiKey
        bitflyer.secret=  self.secret
        trades = bitflyer.fetch_my_trades(
            symbol = settings.symbol,
            params = { "product_code" : settings.product_code}
        )
        return trades

    def fetch_trades_summary(self) -> TradesSummary:
        bitflyer = ccxt.bitflyer()
        bitflyer.apiKey = self.apiKey
        bitflyer.secret=  self.secret
        f_trades = bitflyer.fetch_my_trades(
            symbol = settings.symbol,
            params = { "product_code" : settings.product_code}
        )
        for f_trade in  f_trades:
                tradedata = TradesSummary(
                    side = f_trade["side"],
                    amount = f_trade["amount"],
                    price = f_trade['price'],
                    id = f_trade['info']["child_order_id"],
                )
                print(tradedata.side, tradedata.amount, tradedata.price, tradedata.id )

    def fetch_orders_summary(self) -> OrdersSummary:
        bitflyer = ccxt.bitflyer()
        bitflyer.apiKey = self.apiKey
        bitflyer.secret=  self.secret
        f_orders = bitflyer.fetch_orders(
            symbol = settings.symbol,
            params = { "product_code" : settings.product_code}
        )
        for f_order in f_orders:
            orderdata = OrdersSummary(
                product_code = f_order['info']['product_code'],
                side = f_order["info"]["side"],
                amount = f_order["amount"],
                order_type = f_order["type"],
                price = f_order["price"],
                id = f_order["id"]
            )
            print(orderdata.product_code, orderdata.side, orderdata.amount, orderdata.order_type, orderdata.order_state,orderdata.id)

def get_ticker(symbol ,product_code):
    params = {
        "symbol": symbol,
        "product_code" : product_code
    }

    bitflyer = ccxt.bitflyer()
    ticker = bitflyer.fetch_ticker(symbol = symbol, params = params)
    ask = ticker["ask"]
    bid = ticker["bid"]
    product_code = ticker['info']["product_code"]
    volume = ticker['info']["volume"]
    timestamp = ticker['info']["timestamp"]
    return Ticker(ask, bid, product_code, volume, timestamp)