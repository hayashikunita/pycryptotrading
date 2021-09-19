from functools import partial
import logging

from app.models.candle import create_candle_with_duration
from bitflyer.bitflyer import Ticker
from threading import Lock
from threading import Thread

from app.controllers.ai import AI
import constants
import settings
import time

logger = logging.getLogger(__name__)

# TODO
from bitflyer.bitflyer import APIClient
api = APIClient(settings.apiKey, settings.secret)

 # -------------リアルタイムデータ取得ーーーーーーーーーーーー
 # -*- coding: utf-8 -*-

import json
import websocket
 
def on_message(ws, message):
    r = json.loads(message)['params']['message']
    product_code =r['product_code']
    timestamp=time.time()
    ask=r['best_ask']
    bid=r['best_bid']
    volume = r['volume']
    ticker = Ticker(product_code,timestamp,bid,ask, volume)
    StreamData.trade(ticker)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    print("### open ###")
    ws.send(json.dumps({
            'method': 'subscribe',
            'params': {'channel': 'lightning_ticker_BTC_JPY'},
        }))

 # -------------リアルタイムデータ取得ーーーーーーーーーーーー

class StreamData():

    def __init__(self):
        self.ai = AI(
            product_code=settings.product_code,
            use_percent=settings.use_percent,
            duration=settings.trade_duration,
            past_period=settings.past_period,
            stop_limit_percent=settings.stop_limit_percent,
            back_test=settings.back_test)
        # pyfxtradingの場合
        # self.trade_lock = Lock()
        # pyfxtradingの場合

    def stream_ingestion_data(self):
        ws = websocket.WebSocketApp("wss://ws.lightstream.bitflyer.com/json-rpc",
            on_message=on_message,
            on_error=on_error,
            on_close=on_close)
        ws.on_open = on_open
        ws.run_forever()

    def trade(ticker):
        logger.info(f'action=trade ticker={ticker.__dict__}')
        for duration in constants.DURATIONS:
            is_created = create_candle_with_duration(ticker.product_code, duration, ticker)

            print(is_created) 
            if is_created and duration == settings.trade_duration:

                product_code=settings.product_code
                use_percent=settings.use_percent
                duration=settings.trade_duration
                past_period=settings.past_period
                stop_limit_percent=settings.stop_limit_percent
                back_test=settings.back_test

                ai  = AI(
                    product_code,
                    use_percent,
                    duration,
                    past_period,
                    stop_limit_percent,
                    back_test)

                thread = Thread(target=StreamData._trade, args=(StreamData, ai,))
                thread.start()
                print("aaaaa")

    def _trade(self, ai:AI):
        # pyfxtradingの場合
        # with self.trade_lock:
        # pyfxtradingの場合
        ai.trade()

# singleton
stream = StreamData()