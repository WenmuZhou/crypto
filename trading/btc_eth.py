#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/3/29 10:35
# @Author  : Adolf
# @File    : btc_eth.py
import ccxt
import time
import pandas as pd
import talib

exchange = ccxt.binance()

exchange.apiKey = "e3cDWMh8N1uugwePjZK0OLZ73dMCl45kX7kIbniN9kjx42r5UtBAGs1S6JKvEXiu"
exchange.secret = "F6OShDNksFqTqCqD8mGbAEmi7sDubGWxHakra3nA8xVn3RWbw9qsDqNMi75OhNVG"


def auto_trade():
    balance = exchange.fetch_balance()
    balance_my = dict()

    for coin in balance["info"]["balances"]:
        if coin["asset"] in ["USDT", "BTC", "ETH"]:
            print(coin)
            balance_my[coin["asset"]] = float(coin["free"])

    momentum_days = 20

    data_btc = exchange.fetch_ohlcv("BTC/USDT", timeframe="1d", limit=30)
    date_eth = exchange.fetch_ohlcv("ETH/USDT", timeframe="1d", limit=30)

    df_btc = pd.DataFrame(data_btc, columns=["time", "open", "high", "low", "close", "vol"])
    df_eth = pd.DataFrame(date_eth, columns=["time", "open", "high", "low", "close", "vol"])

    # df['time_stamp'] = pd.to_datetime(df["time_stamp"], unit="ms")
    df_btc['btc_pct'] = df_btc['close'].pct_change(1)
    df_eth['eth_pct'] = df_eth['close'].pct_change(1)

    df_btc.rename(columns={'open': 'btc_open', 'close': 'btc_close'}, inplace=True)
    df_eth.rename(columns={'open': 'eth_open', 'close': 'eth_close'}, inplace=True)

    df = pd.merge(left=df_btc[['time', 'btc_open', 'btc_close', 'btc_pct']],
                  left_on=['time'],
                  right=df_eth[['time', 'eth_open', 'eth_close', 'eth_pct']],
                  right_on=['time'],
                  how='left')

    df['btc_mom'] = df['btc_close'].pct_change(periods=momentum_days)
    df['eth_mom'] = df['eth_close'].pct_change(periods=momentum_days)

    df['time_stamp'] = pd.to_datetime(df["time"], unit="ms")

    df.loc[df['btc_mom'] > df['eth_mom'], 'style'] = 'btc'
    df.loc[df['btc_mom'] < df['eth_mom'], 'style'] = 'eth'
    df.loc[(df['btc_mom'] < 0) & (df['eth_mom'] < 0), 'style'] = 'usdt'

    # print(df)

    now_style = df["style"][len(df) - 1]
    print(now_style)
    print(balance_my)

    if now_style == "btc":
        if balance_my["ETH"] != 0:
            exchange.create_market_sell_order(symbol="ETH/BTC", amount=balance_my["ETH"])
        elif balance_my["USDT"] > 1:
            trick = exchange.fetch_ticker(symbol="BTC/USDT")
            # print(trick["ask"])
            exchange.create_limit_buy_order(symbol="BTC/USDT", price=trick["ask"],
                                            amount=balance_my["USDT"] / trick["ask"])
    elif now_style == "eth":
        if balance_my["BTC"] != 0:
            exchange.create_market_sell_order(symbol="BTC/ETH", amount=balance_my["BTC"])
        elif balance_my["USDT"] > 1:
            trick = exchange.fetch_ticker(symbol="ETH/USDT")
            exchange.create_limit_buy_order(symbol="ETH/USDT", price=trick["ask"],
                                            amount=balance_my["USDT"] / trick["ask"])
    else:
        if balance_my["BTC"] != 0:
            exchange.create_market_sell_order(symbol="BTC/USDT", amount=balance_my["BTC"])
        elif balance_my["ETH"] != 0:
            exchange.create_market_sell_order(symbol="ETH/USDT", amount=balance_my["ETH"])


while True:
    # now_time = time.time()
    # if int(now_time) % 86400000 < 10000:
    auto_trade()
    time.sleep(400000)
    # time.sleep(86399998)
    # else:
    #     time.sleep(10000)
