#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/4/14 10:42
# @Author   : Adolf
# @File     : turn_mul.py
# @Function  :
import ccxt
import pandas as pd
import datetime
from trading.utils import post_msg_to_dingtalk, get_balance_info

exchange = ccxt.binance()

# me
# exchange.apiKey = "e3cDWMh8N1uugwePjZK0OLZ73dMCl45kX7kIbniN9kjx42r5UtBAGs1S6JKvEXiu"
# exchange.secret = "F6OShDNksFqTqCqD8mGbAEmi7sDubGWxHakra3nA8xVn3RWbw9qsDqNMi75OhNVG"

# wenmu
exchange.apiKey = "J0p53QWHzOaU6h7ZmmGukFfJ7C97tN3rhhs7s3jFmZJ2rNHZvxYvoYDHklMrWWZq"
exchange.secret = "0MOMZJC3fNW0FsDL5Xu3qj2YNK8dPVqDgbxqR3USCi396uy1aCXxW2Tto78nuGWA"

coin_list = ["BTC", "ETH", "EOS", "XRP", "DOT", "BNB", "ADA", "UNI"]


def auto_trade_v2(coin_list):
    balance_my, max_value_coin, balance_my_value = get_balance_info(coin_list, exchange)
    momentum_days = 5

    coin_mom = {}
    for coin_name in coin_list:
        data = exchange.fetch_ohlcv(coin_name + "/USDT", timeframe="4h", limit=30)
        df = pd.DataFrame(data, columns=["time", "open", "high", "low", "close", "vol"])

        df['coin_pct'] = df['close'].pct_change(1)
        df['coin_mom'] = df['close'].pct_change(periods=momentum_days)
        # print(df)
        # print(df.tail(1)["coin_mom"].item())
        coin_mom[coin_name] = df.tail(1)["coin_mom"].item()

    max_value = max(coin_mom.values())
    for keys, values in coin_mom.items():
        if values == max_value:
            # print(keys, values)
            now_style = keys
            if max_value <= 0:
                now_style = "USDT"

    print("now_style:", now_style)
    print("origin balance:", balance_my)
    print("origin position:", max_value_coin)
    max_value_coin_new = max_value_coin
    if max_value_coin != now_style:
        while max_value_coin_new != "USDT":
            trick = exchange.fetch_ticker(symbol=max_value_coin + "/USDT")
            exchange.create_limit_sell_order(symbol=max_value_coin + "/USDT", price=trick["bid"],
                                             amount=balance_my[max_value_coin])
            balance_my_new, max_value_coin_new = get_balance_info(coin_list, exchange)

        if now_style != "USDT":
            trick = exchange.fetch_ticker(symbol=now_style + "/USDT")
            exchange.create_limit_buy_order(symbol=now_style + "/USDT", price=trick["ask"],
                                            amount=balance_my["USDT"] / trick['ask'])

    balance_my_new, max_value_coin_new, balance_my_value = get_balance_info(coin_list, exchange)
    post_msg_to_dingtalk(
        msg="当前时间：{},原来持有的币种：{},买入的新币种为：{},账户余额：{}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                                           max_value_coin, max_value_coin_new, balance_my_value * 6.72))
    # balance_my_new, max_value_coin_new = get_balance_info(coin_list)
    # print("balance_my_new", balance_my_new)
    # print("max_value_coin_new", max_value_coin_new)


# auto_trade_v2(coin_list)

balance_my_new, max_value_coin_new, balance_my_value = get_balance_info(coin_list, exchange)
print("balance_my_new:", balance_my_new)
print("max_value_coin_new:", max_value_coin_new)
print("balance_my_value:", balance_my_value)

# post_msg_to_dingtalk(msg="test!test!")
