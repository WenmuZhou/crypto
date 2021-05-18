# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @Project : crypto
# @Date    : 2021/5/15 22:21
# @Author  : Adolf
# @File    : turn_strategy.py
# @Function:
import os

import pandas as pd
from functools import reduce

pd.set_option("expand_frame_repr", False)
pd.set_option("display.max_rows", 1000)

coin_list = ["BTC", "ETH", "EOS", "FIL", "LTC", "ETC", "BCH", "BAT",
             "XRP", "DOT", "KSM", "CAKE", "BNB", "LINK", "ADA", "UNI",
             "CHZ", "DOGE", "MATIC"]
# momentum_day = 5
trade_rate = 2 / 1000
time_period = "15m"


def cal_mom(_momentum_day, _coin_list):
    data_frames = []
    for coin_name in _coin_list:
        df_dir = "dataset/" + time_period + "/" + coin_name + "_USDT_" + time_period
        df_list = os.listdir(df_dir)
        # exit()
        df = pd.read_csv(os.path.join(df_dir, df_list[0]))
        del df['time'], df['high'], df['low'], df['vol']
        df = df[['time_stamp', 'open', 'close']]
        df[coin_name + '_pct'] = df['close'].pct_change(periods=1)
        df[coin_name + '_momentum'] = df['close'].pct_change(periods=_momentum_day)
        df.rename(columns={'open': coin_name + '_open',
                           'close': coin_name + '_close'},
                  inplace=True)
        # print(df)
        data_frames.append(df)

    df_merged = reduce(lambda left, right: pd.merge(left, right, on=['time_stamp'],
                                                    how='outer'), data_frames)
    df_merged.sort_values(by=['time_stamp'], inplace=True)
    print('共使用K线:', len(df_merged))
    df_merged["USDT_close"] = 1
    df_merged["USDT_pct"] = 0
    _my_position = {"date": "2018-07-19",
                    "pre_close": 1,
                    "pre_style": "USDT",
                    "style_close": 1,
                    "pos_style": "USDT",
                    "my_value": 1,
                    "is_turn": False}

    for index, row in df_merged.iterrows():
        _my_position["date"] = row["time_stamp"]
        max_momentum = 0
        coin_style = "USDT"
        for coin_name in _coin_list:
            if not pd.isnull(row[coin_name + '_momentum']):
                # print(coin_name)
                if row[coin_name + '_momentum'] > max_momentum:
                    max_momentum = row[coin_name + '_momentum']
                    coin_style = coin_name
        _my_position["pre_close"] = _my_position["style_close"]
        _my_position["pre_style"] = _my_position["pos_style"]

        # my_position["style_close"] = row[my_position["pos_style"] + "_close"]
        # my_position["my_value"] *= (1 + my_position["style_close"] / my_position["pre_close"])
        _my_position["is_turn"] = False

        if max_momentum > 0 and _my_position["pos_style"] != coin_style:
            _my_position["my_value"] *= (1 - trade_rate)
            _my_position["pos_style"] = coin_style
            _my_position["is_turn"] = True

        _my_position["style_close"] = row[_my_position["pos_style"] + "_close"]
        if not _my_position["is_turn"]:
            _my_position["my_value"] *= (1 + row[_my_position["pos_style"] + "_pct"])
        else:
            _my_position["my_value"] *= (1 + row[_my_position["pre_style"] + "_pct"])
        # print(_my_position)
    return _my_position


for i in range(3, 61):
    print(i)
    my_position = cal_mom(_momentum_day=i, _coin_list=coin_list)
    print(my_position["my_value"])
    # break
