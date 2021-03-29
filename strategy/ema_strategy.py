#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/3/29 19:37
# @Author  : Adolf
# @File    : ema_strategy.py
import talib
import numpy as np
import pandas as pd

coin_name = "BTC"
history_df = pd.read_csv("dataset/day/" + coin_name + ".csv")

ma_len = 10
history_df["EMA"] = talib.EMA(history_df["close"], timeperiod=ma_len)
history_df["SMA"] = talib.SMA(history_df["close"], timeperiod=ma_len)

# print(history_df)
start_new = {"USDT": 100,
             coin_name: 0}

print(len(history_df))

for index, row in history_df.iterrows():
    # print(row)
    pass
# print(start_new)
# print("币价值自身变化", history_df['close'][len(history_df) - 1] / history_df['open'][0])
# print("最终剩余价值", (row["close"] * start_new[coin_name] + start_new["USDT"]) / 100)
