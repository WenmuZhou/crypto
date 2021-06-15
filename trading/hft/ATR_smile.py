#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Project : crypto
# @Date    : 2021/6/5 14:29
# @Author  : Adolf
# @File    : ATR_smile.py
# @Function:
import talib
from trading.trade_strategy.base_trading import BasisTrading


class ATRSmile(BasisTrading):
    def strategy_trade(self, params):
        coin_name = params.get("coin_name", "BTC")
        upper_band = params.get("upper_band", 20)
        lower_band = params.get("lower_band", 10)
        time_periods = params.get("time_periods", "4h")

        df = self.get_data(coin_name, time_periods, max(upper_band, lower_band) * 2)

        df['upper_band'] = talib.MAX(df.high, timeperiod=upper_band).shift(1)
        df['lower_band'] = talib.MIN(df.low, timeperiod=lower_band).shift(1)
        # print(df)
        print(df.tail(1))

        if df.tail(1)["close"].item() > df.tail(1)["upper_band"].item():
            now_style = coin_name + "UP"
        elif df.tail(1)["close"].item() < df.tail(1)["lower_band"].item():
            now_style = coin_name + "DOWN"
        else:
            now_style = "USDT"
        return now_style


if __name__ == '__main__':
    auto_trade = TurtleTrade(post_to_ding_talk=False)
    # auto_trade.trading_main(coin_name="BTC", user="yujl", upper_band=20, lower_band=10, time_periods="1d")
    params = {"coin_name": "BTC",
              "upper_band": 20,
              "lower_band": 10,
              "time_periods": "1d"}
    print(auto_trade.strategy_trade(params))
