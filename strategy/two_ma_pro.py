#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/4/6 9:58
# @Author  : Adolf
# @File    : two_ma_pro.py
import os
import ray
from tqdm import tqdm, trange
import talib
import pandas as pd
import mplfinance as mpf

# ray.init()

pd.set_option("expand_frame_repr", False)
pd.set_option("display.max_rows", 1000)

trade_rate = 1.5 / 1000


def main_two_ma_strategy(coin_name_, short_period_, long_period_):
    df = pd.read_csv("dataset/1d/" + coin_name_ + ".csv")
    df["ma_short"] = talib.SMA(df["close"], timeperiod=short_period_)
    df["ma_long"] = talib.SMA(df["close"], timeperiod=long_period_)
    df.rename(columns={"vol": "volume"}, inplace=True)
    df["Date"] = df["time_stamp"]
    df.set_index("Date", inplace=True)
    df.index = pd.to_datetime(df.index)
    # print(df)
    df["coin_pct"] = df["close"].pct_change(1)

    df.loc[(df['ma_short'] > df["ma_long"]) & (df["ma_short"].shift(1) < df["ma_long"].shift(1)), "signal_long"] = df[
        "close"]
    df.loc[(df['ma_short'] < df["ma_long"]) & (df["ma_short"].shift(1) > df["ma_long"].shift(1)), "signal_short"] = df[
        "close"]

    df.loc[(df['ma_short'] > df["ma_long"]) & (df["ma_short"].shift(1) < df["ma_long"].shift(1)), "style"] = "buy"
    df.loc[(df['ma_short'] < df["ma_long"]) & (df["ma_short"].shift(1) > df["ma_long"].shift(1)), "style"] = "sell"

    df['style'].fillna(method="pad", inplace=True)
    df["pos"] = df["style"].shift(1)

    df.loc[df['pos'] == 'buy', 'strategy_pct'] = df['coin_pct']
    df.loc[df['pos'] == 'sell', 'strategy_pct'] = 0

    df.loc[(df['pos'] != df['pos'].shift(1)) & (df["pos"].notnull()) & (df["pos"].shift(1).notnull()), \
           'trade_time'] = df['time_stamp']

    df.loc[df['pos'] != df['pos'].shift(1), 'trade_time'] = df['time_stamp']
    del df["style"], df["time_stamp"]

    # 扣除卖出手续费
    df.loc[(df['trade_time'].notnull()), 'strategy_pct'] = (1 + df[
        'strategy_pct']) * (1 - trade_rate) - 1

    df['coin_net'] = df['close'] / df['close'][long_period_]
    df['strategy_net'] = (1 + df['strategy_pct']).cumprod()

    coin_net_ = df.tail(1)["coin_net"].item()
    strategy_net_ = df.tail(1)["strategy_net"].item()
    # print("coin_net:", coin_net_)
    # print("strategy_net:", strategy_net_)
    # df.to_csv("result/reef_4h_6_45.csv")
    return coin_net_, strategy_net_


def plot_image(df_):
    my_color = mpf.make_marketcolors(up="red", down="green", edge="inherit", volume="inherit")
    my_style = mpf.make_mpf_style(marketcolors=my_color)

    add_plot = [mpf.make_addplot(df_[['ma_short', 'ma_long']]),
                mpf.make_addplot(df_['signal_long'], scatter=True, marker="^", color="r"),
                mpf.make_addplot(df_['signal_short'], scatter=True, marker="v", color="g")]
    mpf.plot(df_, type="line", ylabel="price(usdt)", style=my_style, volume=True, ylabel_lower="vol",
             addplot=add_plot)


# coin_list = ["BTC", "ETH", "EOS", "LTC", "XRP", "BNB", "DOT", "FIL"]
coin_list = ["BTC"]


# for coin_name in coin_list:
#     short_period = 7
#     long_period = 25
#     print(coin_name)
#     coin_net, strategy_net = main_two_ma_strategy(coin_name_=coin_name, long_period_=long_period,
#                                                   short_period_=short_period)

@ray.remote
def ray_accelerate(coin_name):
    res_item = []
    for short_period in range(3, 201):
        for long_period in range(7, 251):
            if short_period >= long_period:
                continue
            coin_net, strategy_net = main_two_ma_strategy(coin_name_=coin_name, long_period_=long_period,
                                                          short_period_=short_period)
            res_item.append([coin_name, short_period, long_period, coin_net, strategy_net, strategy_net > coin_net])

    return res_item


def simple_test(coin_list):
    tqdm_coin_list = tqdm(coin_list)
    res = []
    for coin_name in tqdm_coin_list:
        for short_period in trange(3, 180):
            for long_period in range(7, 240):
                tqdm_coin_list.set_description("Now Processing %s" % coin_name)
                if short_period >= long_period:
                    continue
                coin_net, strategy_net = main_two_ma_strategy(coin_name_=coin_name, long_period_=long_period,
                                                              short_period_=short_period)
                res.append([coin_name, short_period, long_period, coin_net, strategy_net, strategy_net > coin_net])
    print("short_period:", short_period)
    print("long_period:", long_period)
    print("coin_net:", coin_net)
    print("strategy_net:", strategy_net)
    print("=============================")

    # res_df = pd.DataFrame(res, columns=["coin", "short_period", "long_period", "coin_net", "strategy_net", "is_win"])
    # res_df.to_csv("result/two_ma_pro_reef_4h.csv", index=False)


# simple_test(coin_list)
coin_net, strategy_net = main_two_ma_strategy("BTC", 5, 10)
print("coin_net", coin_net)
print("strategy_net", strategy_net)


def ray_use(coin_list):
    ray.init()
    futures = [ray_accelerate.remote(i) for i in coin_list]
    res = ray.get(futures)[0]
    # print(res)
    res_df = pd.DataFrame(res, columns=["coin", "short_period", "long_period", "coin_net", "strategy_net", "is_win"])
    # print(res_df)
    res_df.to_csv("result/two_ma_pro_15min.csv", index=False)
