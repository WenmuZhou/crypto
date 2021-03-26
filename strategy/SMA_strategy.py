#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/3/26 15:21
# @Author  : Adolf
# @File    : SMA_strategy.py
import ccxt
import talib
import pandas as pd

exchange = ccxt.okex()

# data = exchange.fetch_ohlcv("EOS/USDT", timeframe="15m", limit=1500)

# print(data)
# df = pd.DataFrame(data, columns=["time_stamp", "open", "high", "low", "close", "vol"])
# df['time_stamp'] = pd.to_datetime(df["time_stamp"], unit="ms")
# print(df)
# df.to_csv("dataset/ecos_15min.csv", index=False)
# real = talib.SMA(df["close"], timeperiod=10)
# print(real)
history_df = pd.read_csv("dataset/Binance_EOSUSDT_1h.csv")
# print(history_df['unix'][1])
history_df["10MA"] = talib.SMA(history_df["close"], timeperiod=10)
history_df["5MA"] = talib.SMA(history_df["close"], timeperiod=5)

print(history_df)

