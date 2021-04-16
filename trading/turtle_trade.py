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
        df['upper_band'] = talib.MAX(df.high, timeperiod=30).shift(1)
        df['lower_band'] = talib.MIN(df.low, timeperiod=20).shift(1)

        now_style = "USDT"
        df.loc[df["close"] > df["upper_band"], "pos"] = "BTC"
        df.loc[df['close'] < df["lower_band"], "pos"] = "USDT"

        turtle_result = df.tail(1)["pos"].item()
        if not np.isnan(turtle_result):
            now_style = turtle_result

        if now_style != max_value_coin:
            trick = exchange.fetch_ticker(symbol="BTCUP/USDT")
            if now_style == "BTC":
                exchange.create_limit_buy_order(symbol="BTCUP/USDT", price=trick["bid"],
                                                amount=balance_my["USDT"] / trick['bid'])
                max_value_coin_new = "BTCUP"

            else:
                exchange.create_market_sell_order(symbol="BTCUP/USDT",
                                                  amount=balance_my["BTCUP"])

                max_value_coin_new = "USDT"

            post_msg_to_dingtalk(title="rich",
                                 msg="当前时间:{},策略名称:{},原来持有的币种:{},买入的新币种为:{},账户余额:{}".format(
                                     datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                     "turtle BTC",
                                     max_value_coin, max_value_coin_new, balance_my_value * 6.72),
                                 token="8392f247561974cf01f63efc77bfeb814c70a00453aee8eb26c405081af03dbe")

        else:
            post_msg_to_dingtalk(title="rich",
                                 msg="当前时间:{},策略名称:{},本次没有调仓,账户余额:{}".format(
                                     datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                     "turtle BTC",
                                     balance_my_value * 6.72),
                                 token="8392f247561974cf01f63efc77bfeb814c70a00453aee8eb26c405081af03dbe")


auto_trade(coin_list, exchange)
