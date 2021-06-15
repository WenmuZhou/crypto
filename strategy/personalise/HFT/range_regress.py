# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @Project : crypto
# @Date    : 2021/5/30 14:56
# @Author  : Adolf
# @File    : range_regress.py
# @Function:
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

pd.set_option("expand_frame_repr", False)
pd.set_option("display.max_rows", 1000)

trade_rate = 1 / 1000


# trade_rate = 0

# k1 = 0.3
# k2 = 0.6
# loss_price = 20
# time_period = 2


def range_strategy(_coin_name, _k1, _k2, _loss_price, _time_period):
    # test_data = "dataset/5m/ETH_USDT_5m/from_2021-03-21_11-35-00_to_2021-05-29_22-10-00.csv"
    test_data_dir = os.path.join("dataset/5m/",_coin_name+"_USDT_5m")
    df = pd.read_csv(os.path.join(test_data_dir,os.listdir(test_data_dir)[0]))
    df = df[:5000]
    del df["time"]
    df = df[["time_stamp", "open", "high", "low", "close"]]

    df["coin_pct"] = df["close"].pct_change(1)
    df['range'] = (df.high.rolling(_time_period).max() - df.low.rolling(_time_period).min()).shift(1)
    df["long_open_price"] = df["open"] - _k1 * df["range"]

    df.dropna(how="any", inplace=True)
    df.reset_index(drop=True, inplace=True)

    holding = False
    for index, row in df.iterrows():
        # print(row)
        if holding:
            if row["low"] < stop_loss_price:
                df.loc[index, "pct"] = stop_loss_price / df.loc[index - 1, "close"] - 1
                df.loc[index, "pct"] = (1 + df.loc[index, "pct"]) * (1 - trade_rate) - 1
                holding = False
            elif row["high"] > stop_win_price:
                holding = False
                df.loc[index, "pct"] = max(row["open"], stop_win_price) / df.loc[index - 1, "close"] - 1
                df.loc[index, "pct"] = (1 + df.loc[index, "pct"]) * (1 - trade_rate) - 1
            else:
                df.loc[index, "pct"] = row["close"] / df.loc[index - 1, "close"] - 1

        else:
            if row["low"] < row["long_open_price"]:
                holding = True
                stop_win_price = row["long_open_price"] + _k2 * row["range"]
                stop_loss_price = row["long_open_price"] * _loss_price
                if row["low"] < stop_loss_price:
                    df.loc[index, "pct"] = stop_loss_price / row["long_open_price"] - 1
                    df.loc[index, "pct"] = (1 + df.loc[index, "pct"]) * (1 - trade_rate) - 1
                    holding = False
                # elif row["close"] > stop_win_price:
                # df.loc[index, "pct"] = stop_win_price / row["long_open_price"] - 1
                # df.loc[index, "pct"] = (1 + df.loc[index, "pct"]) * (1 - trade_rate) - 1
                else:
                    df.loc[index, "pct"] = row["close"] / row["long_open_price"] - 1

            else:
                df.loc[index, "pct"] = 0

    df["strategy_pct"] = (1 + df['pct']).cumprod()
    df["coin_net"] = (1 + df["coin_pct"]).cumprod()

    return df.tail(1)["strategy_pct"].item()

    # plt.plot(df['time_stamp'], df["strategy_pct"], label="strategy_pct")
    # plt.plot(df["time_stamp"], df["coin_net"])
    # plt.show()

# print(range_strategy(_coin_name="BTC", _k1=1.2, _k2=5.6, _loss_price=0.99, _time_period=2))
# coin_list = ["BTC", "ETH", "EOS", "XRP", "DOT", "ADA", "UNI", "DOGE", ]
coin_list = ["BTC"]
for coin_name in coin_list:
    for k1 in np.arange(0.6, 4, 0.1):
        for k2 in np.arange(4, 8, 0.2):
            loss_price = 0.99
            time_period = 2
            strategy_pct = range_strategy(coin_name, k1, k2, loss_price, time_period)
            if strategy_pct < 1:
                continue
            print("coin name:", coin_name)
            print("k1:", k1)
            print("K2:", k2)
            print("strategy_pct", strategy_pct)
            print("=" * 10)
#
# btc:0.6,6.4;0.6,7.2;0.8,6.8;0.8,7.0;1.2,5.4;1.3,5.6
# eos:1.2,5.4
