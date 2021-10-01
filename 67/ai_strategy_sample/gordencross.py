def trade(self):
    logger.info('action=trade status=run')
    # params = self.optimized_trade_params
    # if params is None:
    #     return

    df = DataFrameCandle(self.product_code, self.duration)
    df.set_all_candles(self.past_period)

    ema_values_1 = talib.EMA(np.array(df.closes), timeperiod=5)
    ema_values_2 = talib.EMA(np.array(df.closes), timeperiod=10)

    for i in range(1, len(df.candles)):
        buy_point, sell_point = 0, 0

        # if params.ema_enable and params.ema_period_1 <= i and params.ema_period_2 <= i:
        if ema_values_1[i - 1] < ema_values_2[i - 1] and ema_values_1[i] >= ema_values_2[i]:
            buy_point += 1

        if ema_values_1[i - 1] > ema_values_2[i - 1] and ema_values_1[i] <= ema_values_2[i]:
            sell_point += 1

        if buy_point > 0:
            if not self.buy(df.candles[i]):
                continue

            self.stop_limit = df.candles[i].close * self.stop_limit_percent

        if sell_point > 0 or self.stop_limit > df.candles[i].close:
            if not self.sell(df.candles[i]):
                continue

            self.stop_limit = 0.0
            # self.update_optimize_params(is_continue=True)