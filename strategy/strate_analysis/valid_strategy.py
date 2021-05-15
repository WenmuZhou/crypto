# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @Project : crypto
# @Date    : 2021/5/15 22:21
# @Author  : Adolf
# @File    : valid_strategy.py
# @Function:
import pandas as pd
from functools import reduce

pd.set_option("expand_frame_repr", False)
pd.set_option("display.max_rows", 1000)

coin_list = ["UNI", "FIL", "DOT", "ADA", "BNB", "EOS", "XRP", "KSM", "CAKE"]
# momentum_day = 5
trade_rate = 2 / 1000


def cal_mom(_momentum_day):
    data_frames = []
    for coin_name in coin_list:
        df = pd.read_csv("dataset/4h/" + coin_name + ".csv")
        del df['time'], df['high'], df['low'], df['vol']
        df[coin_name + '_pct'] = df['close'].pct_change(periods=1)
        df[coin_name + '_momentum'] = df['close'].pct_change(periods=_momentum_day)
        df.rename(columns={'open': coin_name + '_open',
                           'close': coin_name + '_close'},
                  inplace=True)
        # print(df)
        data_frames.append(df)

    df_merged = reduce(lambda left, right: pd.merge(left, right, on=['time_stamp'],
                                                    how='outer'), data_frames)
    # print(df_merged)
    df_merged["USDT_close"] = 1
    df_merged["USDT_pct"] = 0
    my_position = {"date": "2018-07-19",
                   "pre_close": 1,
                   "pre_style": "USDT",
                   "style_close": 1,
                   "pos_style": "USDT",
                   "my_value": 1,
                   "is_turn": False}

    for index, row in df_merged.iterrows():
        if row["time_stamp"] == "2020-09-16 20:00:00":
            print(row)
        my_position["date"] = row["time_stamp"]
        max_momentum = 0
        coin_style = "USDT"
        for coin_name in coin_list:
            if not pd.isnull(row[coin_name + '_momentum']):
                # print(coin_name)
                if row[coin_name + '_momentum'] > max_momentum:
                    max_momentum = row[coin_name + '_momentum']
                    coin_style = coin_name
        my_position["pre_close"] = my_position["style_close"]
        my_position["pre_style"] = my_position["pos_style"]

        # my_position["style_close"] = row[my_position["pos_style"] + "_close"]
        # my_position["my_value"] *= (1 + my_position["style_close"] / my_position["pre_close"])
        my_position["is_turn"] = False

        if max_momentum > 0 and my_position["pos_style"] != coin_style:
            my_position["my_value"] *= (1 - trade_rate)
            my_position["pos_style"] = coin_style
            my_position["is_turn"] = True

        my_position["style_close"] = row[my_position["pos_style"] + "_close"]
        if not my_position["is_turn"]:
            my_position["my_value"] *= (1 + row[my_position["pos_style"] + "_pct"])
        else:
            my_position["my_value"] *= (1 + row[my_position["pre_style"] + "_pct"])
        print(my_position)
    return my_position


for i in range(3, 61):
    print(i)
    my_position = cal_mom(_momentum_day=i)
    print(my_position["my_value"])
    break