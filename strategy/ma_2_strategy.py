#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/3/26 15:21
# @Author  : Adolf
# @File    : ma_2_strategy.py
import talib
import numpy as np
import pandas as pd


def ma_2_test(coin_name, long_ma=60, short_ma=30):
    history_df = pd.read_csv("dataset/day/" + coin_name + ".csv")
    coin_name = "coin"
    history_df["LongMA"] = talib.SMA(history_df["close"], timeperiod=long_ma)
    history_df["ShortMA"] = talib.SMA(history_df["close"], timeperiod=short_ma)

    # print(history_df)
    start_new = {"USDT": 100,
                 coin_name: 0}

    history_df.dropna(subset=['LongMA'], inplace=True)
    history_df.reset_index(drop=True, inplace=True)
    # print(len(history_df))
    if len(history_df) == 0:
        return 0, 0

    for index, row in history_df.iterrows():
        # print(row)
        # exit()
        if np.isnan(row['LongMA']) or np.isnan(row["ShortMA"]):
            continue
        # print(row)
        if start_new["USDT"] > 0 and row["ShortMA"] > row["LongMA"]:
            start_new[coin_name] = start_new["USDT"] / row['close']
            start_new["USDT"] = 0
            # print(start_new)
            # break
        if start_new[coin_name] > 0 and row["LongMA"] > row["ShortMA"]:
            start_new["USDT"] = start_new[coin_name] * row["close"]
            start_new[coin_name] = 0

    # print(start_new)
    # print("币价值自身变化", history_df['close'][len(history_df) - 1] / history_df['open'][0])
    # print("最终剩余价值", (row["close"] * start_new[coin_name] + start_new["USDT"]) / 100)
    # print(history_df)
    coin_net = history_df['close'][len(history_df) - 1] / history_df['open'][0]
    strategy_net = (row["close"] * start_new[coin_name] + start_new["USDT"]) / 100

    print("coin name:", coin_name)
    print("time period", short_ma, long_ma)
    print("coin_net", coin_net)
    print("strategy_net", strategy_net)
    return coin_net, strategy_net


# coin_net, strategy_net = ma_2_test(coin_name="BTC", long_ma=25, short_ma=7)
# print("币自身回报", coin_net)
# print("策略收益率", strategy_net)
coin_list = ["BNB", "BTC", "DOT", "EOS", "ETH", "FIL", "LTC", "XRP"]
long_ma_list = [5, 7, 10, 20, 25, 30, 60, 90, 99, 120, 180, 240, 360]
short_ma_list = [3, 5, 7, 10, 20, 25, 30, 50, 60, 90, 99, 120, 180, 240]

fin_list = []
for coin_name in coin_list:
    for long_ma in long_ma_list:
        for short_ma in short_ma_list:
            if long_ma <= short_ma:
                continue
            else:
                coin_net, strategy_net = ma_2_test(coin_name, long_ma=long_ma, short_ma=short_ma)

                if coin_net != 0:
                    res = [coin_name, short_ma, long_ma, coin_net, strategy_net, strategy_net > coin_net]
                    fin_list.append(res)

res_df = pd.DataFrame(fin_list, columns=["币名", "短均线周期", "长均线周期", "币自身回报", "策略回报", "策略是否跑赢大盘"])
res_df.to_csv("result/双均线策略测试.csv", encoding="gbk", index=False)
print(res_df)
