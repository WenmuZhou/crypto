#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/4/6 16:57
# @Author  : Adolf
# @File    : by_turn_mul.py
import pandas as pd
import time
import mplfinance as mlp
import matplotlib as plt

pd.set_option("expand_frame_repr", False)
pd.set_option("display.max_rows", 1000)

momentum_day = 20

coin_list = ["BTC", "ETH", "EOS", "LTC", "XRP"]
res_df = None
for coin_name in coin_list:
    # print(coin_name)
    df = pd.read_csv("dataset/day/" + coin_name + ".csv")
    df[coin_name + '_pct'] = df['close'].pct_change(periods=1)
    df[coin_name + '_momentum'] = df['close'].pct_change(periods=momentum_day)
    del df['high'], df['low'], df['vol']
    df.rename(columns={'open': coin_name + '_open', 'close': coin_name + 'close'}, inplace=True)
    # print(df)
    if res_df is None:
        res_df = df
    else:
        res_df = pd.merge(res_df, df, how='outer', on=['time_stamp'])

res_df = res_df.dropna(how="any")
res_df.reset_index(drop=True, inplace=True)

print(res_df)
for index, row in res_df.iterrows():
    print(row)
    break
