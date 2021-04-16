# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @Project : crypto
# @Date    : 2021/4/16 22:36
# @Author  : Adolf
# @File    : turtle_trade.py
# @Function:
import ccxt
import numpy as np
import pandas as pd
import datetime
import talib
from trading.utils import post_msg_to_dingtalk, get_balance_info
from trading.laboratory import api_key_dict, api_secret_dict

exchange = ccxt.binance()

exchange.apiKey = api_key_dict["yujl"]
exchange.secret = api_secret_dict["yujl"]

coin_list = ["BTC"]


def auto_trade(coin_list_, exchange_):
    balance_my, max_value_coin, balance_my_value = get_balance_info(coin_list_, exchange_)
    for coin_name in coin_list:
        data = exchange.fetch_ohlcv(coin_name + "/USDT", timeframe="1d", limit=30)
        df = pd.DataFrame(data, columns=["time", "open", "high", "low", "close", "vol"])
        print(df)
        df['upper_band'] = talib.MAX(df.high, timeperiod=30).shift(1)
        df['lower_band'] = talib.MIN(df.low, timeperiod=20).shift(1)

        now_style = "USDT"
        df.loc[df["close"] > df["upper_band"], "pos"] = "BTC"
        df.loc[df['close'] < df["lower_band"], "pos"] = "USDT"

        print(df)
        turtle_result = df.tail(1)["pos"]
        if not np.isnan(turtle_result):
            now_style = turtle_result
            print('1111')

        print(now_style)

auto_trade(coin_list, exchange)
