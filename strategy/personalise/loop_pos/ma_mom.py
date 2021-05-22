#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/5/20 15:56
# @Author   : Adolf
# @File     : ma_mom.py
# @Function  :
import pandas as pd

pd.set_option("expand_frame_repr", False)
pd.set_option("display.max_rows", 1000)

df = pd.read_csv("dataset/stock/600570.csv")
del df["amount"], df["turn"], df["pctChg"], df["adjustflag"]
df = df[-1000:]
df.reset_index(inplace=True)

df['pct'] = df['close'].pct_change(periods=1)
df['short_mom'] = df['close'].pct_change(periods=5)
df['long_mom'] = df['close'].pct_change(periods=10)

print(df)

