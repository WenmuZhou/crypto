#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/5/5 15:32
# @Author   : Adolf
# @File     : down50percentage.py
# @Function  :
import pandas as pd
import numpy as np

pd.set_option("expand_frame_repr", False)
pd.set_option("display.max_rows", 2000)


def down50off(stock_name, time_periods, threshold, stoploss, stopwin):
    df = pd.read_csv("/root/adolf/dataset/d_pre/" + stock_name)
    df.reset_index(drop=True, inplace=True)
    del df['amount'], df["turn"], df["adjustflag"], df["pctChg"]

    # history_high = now_high = df['close'][0]
    df["pct"] = df["close"].pct_change(periods=1)
    now_high = df['close'][0]
    my_position = {"is_pos": False,
                   "buy_price": 0,
                   "my_value": 1,
                   "hold_day": 0, }

    buy_date_list = []
    sell_date_list = []

    for index, row in df.iterrows():
        if row["high"] > now_high:
            now_high = row["high"]
        if (row["low"] < (now_high * threshold)) and not my_position["is_pos"]:
            # print(row.values)
            buy_date_list.append(row["date"])
            my_position["is_pos"] = True
            my_position["buy_price"] = row["close"]
            my_position["hold_day"] = 0
            now_high = row["high"]

        if my_position["is_pos"]:
            my_position["my_value"] = (1 + row["pct"]) * my_position["my_value"]
            my_position["hold_day"] += 1
            if row["close"] < my_position['buy_price'] * stoploss or my_position["hold_day"] > time_periods \
                    or row["close"] > my_position['buy_price'] * stopwin:
                my_position["is_pos"] = False
                sell_date_list.append(row["date"])
                # print(row["date"], "本次获取收益：", row["close"] / my_position["buy_price"])

    return my_position
    # print(my_position)
    # print(buy_date_list)
    # print(sell_date_list)


if __name__ == '__main__':
    # stock_name = "sz.000538.csv"
    time_periods = 10
    threshold = 0.5
    stoploss = 0.95
    stopwin = 100

    import os

    stock_list = os.listdir("/root/adolf/dataset/d_pre/")
    for stock_name in stock_list:
        my_position = down50off(stock_name=stock_name, time_periods=time_periods,
                                threshold=threshold, stoploss=stoploss, stopwin=stopwin)
        print(stock_name)
        print(my_position['my_value'])
        print('=' * 50)
