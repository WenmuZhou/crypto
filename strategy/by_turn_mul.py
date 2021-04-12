#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/4/6 16:57
# @Author  : Adolf
# @File    : by_turn_mul.py
# import numpy as np
import pandas as pd

# import time
# import mplfinance as mlp
# import matplotlib as plt

pd.set_option("expand_frame_repr", False)
pd.set_option("display.max_rows", 1000)

trade_rate = 1.5 / 1000


def turn_strategy(coin_list_, momentum_day_):
    res_df = None
    for coin_name in coin_list_:
        # print(coin_name)
        df_ = pd.read_csv("dataset/day/" + coin_name + ".csv")
        df_[coin_name + '_pct'] = df_['close'].pct_change(periods=1)
        df_[coin_name + '_momentum'] = df_['close'].pct_change(periods=momentum_day_)
        # print(df_)
        df_['time_stamp'] = pd.to_datetime(df_["time"], unit="ms")
        del df_['high'], df_['low'], df_['vol'], df_['time']
        df_ = df_[["time_stamp", "open", "close", coin_name + '_pct', coin_name + '_momentum']]
        df_.rename(columns={'open': coin_name + '_open', 'close': coin_name + '_close'}, inplace=True)
        # print(df)
        if res_df is None:
            res_df = df_
        else:
            print(res_df)
            print(df_)
            res_df = pd.merge(left=res_df, right=df_, how='left', left_on=['time_stamp'], right_on=["time_stamp"])

    res_df = res_df.dropna(how="any")
    res_df.reset_index(drop=True, inplace=True)

    print(res_df)
    exit()
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
    return res_df


# coin_list = ["BTC", "ETH", "EOS", "LTC", "XRP"]
coin_list = ["BTC", "ETH"]
# momentum_day = 18
# for momentum_day in range(3, 31):
#     df = turn_strategy(coin_list, momentum_day_=momentum_day)
#     print(momentum_day, df.tail(1)["strategy_net"].item())
df = turn_strategy(coin_list, momentum_day_=20)
print(df.tail)

df.to_csv('result/20_btc_eth_ltc_bnb_turn.csv', index=False)
