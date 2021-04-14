#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/4/14 10:42
# @Author   : Adolf
# @File     : turn_mul.py
# @Function  :
import ccxt
import pandas as pd

exchange = ccxt.binance()

# me
exchange.apiKey = "e3cDWMh8N1uugwePjZK0OLZ73dMCl45kX7kIbniN9kjx42r5UtBAGs1S6JKvEXiu"
exchange.secret = "F6OShDNksFqTqCqD8mGbAEmi7sDubGWxHakra3nA8xVn3RWbw9qsDqNMi75OhNVG"


def auto_trade_v2():
    balance = exchange.fetch_balance()
    balance_my = dict()

    for coin in balance["info"]["balances"]:
        if coin["asset"] in ["USDT", "BTC", "ETH"]:
            print(coin)
            balance_my[coin["asset"]] = float(coin["free"])

    momentum_days = 10
    print(balance_my)

    coin_list = ["BTC", "ETH", "EOS", "XRP", "DOT", "BNB", "ADA", "UNI"]
    coin_mom = {}
    for coin_name in coin_list:
        data = exchange.fetch_ohlcv(coin_name + "/USDT", timeframe="1d", limit=30)
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

    print(now_style)


auto_trade_v2()
