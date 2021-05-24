#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/5/20 15:56
# @Author   : Adolf
# @File     : ma_mom.py
# @Function  :
import pandas as pd
# import talib
import json

pd.set_option("expand_frame_repr", False)
pd.set_option("display.max_rows", 1000)

df = pd.read_csv("dataset/stock/600570.csv", index_col=False)
del df["amount"], df["turn"], df["pctChg"], df["adjustflag"]
df = df[-1000:]
df.reset_index(inplace=True)

# df['pct'] = df['close'].pct_change(periods=1)
# df['short_mom'] = df['close'].pct_change(periods=5)
# df['long_mom'] = df['close'].pct_change(periods=10)

df["MA5"] = df["close"].rolling(5).mean()
df['MA10'] = df["close"].rolling(10).mean()
# df['MA10_talib'] = talib.MA(df["close"], timeperiod=10)
# df["MACD"] = talib.MACD(df["close"], fastperiod=12, slowperiod=26, signalperiod=9)
df['trade'] = ""
df.loc[(df["MA5"] > df["MA10"]) & (df["MA5"].shift(1) < df["MA10"].shift(1)), "trade"] = "b"
df.loc[(df["MA5"] < df["MA10"]) & (df["MA5"].shift(1) > df["MA10"].shift(1)), "trade"] = "s"

df['diff'] = df["MA5"] - df["MA10"]
df['diff'] = df['diff'].fillna(0)
df["area"] = 0
# print(df)

area_ma = 0
for index, row in df.iterrows():
    # print(row)
    df.loc[index, "area"] = area_ma
    if row["trade"] != "b" and row["trade"] != "s":
        area_ma += row["diff"]
    else:
        area_ma = row["diff"]

print(df)
