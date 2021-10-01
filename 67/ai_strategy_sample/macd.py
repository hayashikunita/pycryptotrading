def trade(self)
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