#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/4/6 16:57
# @Author  : Adolf
# @File    : by_turn_mul.py
import numpy as np
import pandas as pd
import time
import mplfinance as mlp
import matplotlib as plt

pd.set_option("expand_frame_repr", False)
pd.set_option("display.max_rows", 1000)

momentum_day = 18
trade_rate = 1.5 / 1000

# coin_list = ["BTC", "ETH", "EOS", "LTC", "XRP"]
coin_list = ["BTC", "ETH", "XRP"]
res_df = None
for coin_name in coin_list:
    # print(coin_name)
    df = pd.read_csv("dataset/day/" + coin_name + ".csv")
    df[coin_name + '_pct'] = df['close'].pct_change(periods=1)
    df[coin_name + '_momentum'] = df['close'].pct_change(periods=momentum_day)
    del df['high'], df['low'], df['vol']
    df.rename(columns={'open': coin_name + '_open', 'close': coin_name + '_close'}, inplace=True)
    # print(df)
    if res_df is None:
        res_df = df
    else:
        res_df = pd.merge(res_df, df, how='outer', on=['time_stamp'])

res_df = res_df.dropna(how="any")
res_df.reset_index(drop=True, inplace=True)

# print(res_df)
for index, row in res_df.iterrows():
    nb_coin_name = "empty"
    max_mom = 0
    for coin_name in coin_list:
        if row[coin_name + '_momentum'] > max_mom:
            max_mom = row[coin_name + '_momentum']
            nb_coin_name = coin_name
    # print(nb_coin_name)
    # print(max_mom)
    if max_mom > 0:
        res_df.loc[index, "style"] = nb_coin_name
    else:
        res_df.loc[index, "style"] = "empty"

res_df['pos'] = res_df['style'].shift(1)
res_df.dropna(subset=['pos'], inplace=True)

res_df.loc[res_df['pos'] != res_df['pos'].shift(1), 'trade_time'] = res_df['time_stamp']

for index, row in res_df.iterrows():
    # print(row["pos"])
    # print(row[row['pos'] + '_pct'])
    if row["pos"] == "empty":
        res_df.loc[index, "strategy_pct"] = 0.0
    elif isinstance(row["trade_time"], str):
        res_df.loc[index, "strategy_pct"] = row[row["pos"] + '_close'] / (
                row[row["pos"] + '_open'] * (1 + trade_rate)) - 1
    else:
        res_df.loc[index, "strategy_pct"] = row[row["pos"] + '_pct']
    # break
# # 扣除卖出手续费
res_df.loc[(res_df['trade_time'].shift(-1).notnull()) & (res_df["pos"] != "empty"), 'strategy_pct'] = \
    (1 + res_df['strategy_pct']) * (1 - trade_rate) - 1
res_df.reset_index(drop=True, inplace=True)
for coin_name in coin_list:
    res_df[coin_name + '_net'] = res_df[coin_name + '_close'] / res_df[coin_name + '_close'][0]
res_df['strategy_net'] = (1 + res_df['strategy_pct']).cumprod()
print(res_df.tail(1))

# res_df.to_csv('result/数字货币轮动_测试.csv', index=False)
