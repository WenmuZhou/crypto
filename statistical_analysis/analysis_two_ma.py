#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/4/9 16:50
# @Author   : Adolf
# @File     : analysis_two_ma.py
# @Function  :
import pandas as pd

pd.set_option("expand_frame_repr", False)
pd.set_option("display.max_rows", 2000)

# print(df)
# print(df["is_win"].count())
# print(df.describe())
df1 = pd.read_csv("dataset/1d/ETH.csv")
df1['coin1_pct'] = df1['close'].pct_change(periods=1)
df1['coin1_momentum'] = df1['close'].pct_change(periods=20)
# print(df_)
df1['time_stamp'] = pd.to_datetime(df1["time"], unit="ms")
del df1['high'], df1['low'], df1['vol'], df1['time']
df1 = df1[["time_stamp", "open", "close", 'coin1_pct', 'coin1_momentum']]
df1.rename(columns={'open': 'coin1_open', 'close': 'coin1_close'}, inplace=True)

df2 = pd.read_csv("dataset/1d/BTC.csv")
df2['coin2_pct'] = df2['close'].pct_change(periods=1)
df2['coin2_momentum'] = df2['close'].pct_change(periods=20)
df2['time_stamp'] = pd.to_datetime(df2["time"], unit="ms")
del df2['high'], df2['low'], df2['vol'], df2['time']
df2 = df2[["time_stamp", "open", "close", 'coin2_pct', 'coin2_momentum']]
df2.rename(columns={'open': 'coin2_open', 'close': 'coin2_close'}, inplace=True)
print(df1)
print(df2)
print(df1["time_stamp"] == df2["time_stamp"])

res_df = pd.merge(left=df1, right=df2, how='outer', on=['time_stamp'])
res_df.drop_duplicates(inplace=True)
print(res_df)
