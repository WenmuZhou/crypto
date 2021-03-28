#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/3/26 15:21
# @Author  : Adolf
# @File    : SMA_strategy.py
import ccxt
import talib
import numpy as np
import pandas as pd

exchange = ccxt.binance()

history_df = pd.read_csv("dataset/4hour/ETH_4hour.csv")
long_ma = 20
short_ma = 10
coin_name = "coin"
history_df["LongMA"] = talib.SMA(history_df["close"], timeperiod=long_ma)
history_df["ShortMA"] = talib.SMA(history_df["close"], timeperiod=short_ma)

# print(history_df)
start_new = {"USDT": 100,
             coin_name: 0}

# print(len(history_df))

for index, row in history_df.iterrows():
    # print(row)
    # exit()
    if np.isnan(row['LongMA']) or np.isnan(row["ShortMA"]):
        continue
    # print(row)
    if start_new["USDT"] > 0 and row["ShortMA"] > row["LongMA"]:
        start_new[coin_name] = start_new["USDT"] / row['close']
        start_new["USDT"] = 0
        # print(start_new)
        # break
    if start_new[coin_name] > 0 and row["LongMA"] > row["ShortMA"]:
        start_new["USDT"] = start_new[coin_name] * row["close"]
        start_new[coin_name] = 0

# print(start_new)
print("币价值自身变化", history_df['close'][len(history_df) - 1] / history_df['open'][0])
print("最终剩余价值", (row["close"] * start_new[coin_name] + start_new["USDT"])/100)
