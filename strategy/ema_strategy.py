#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/3/29 19:37
# @Author  : Adolf
# @File    : ema_strategy.py
import talib
import numpy as np
import pandas as pd

trade_rate = 1.5 / 1000


def ema_test(coin_name_, ma_len=10, mode="SMA"):
    df = pd.read_csv("dataset/day/" + coin_name_ + ".csv")

    df["EMA"] = talib.EMA(df["close"], timeperiod=ma_len)
    df["SMA"] = talib.SMA(df["close"], timeperiod=ma_len)

    # df.dropna(subset=['EMA', 'SMA'], inplace=True)

    df['coin_pct'] = df['close'].pct_change(1)

    df.loc[df['close'] > df[mode], 'style'] = "buy"
    df.loc[df['close'] < df[mode], 'style'] = "sell"

    df['pos'] = df['style'].shift(1)

    del df['style']

    df.dropna(subset=['pos'], inplace=True)
    df.reset_index(drop=True, inplace=True)

    if len(df) == 0:
        return 0, 0

    df.loc[df['pos'] != df['pos'].shift(1), 'trade_time'] = df['time_stamp']

    if df.loc[0, 'pos'] == "sell":
        df.loc[0, "trade_time"] = None

    # # 将调仓日的涨跌幅修正为开盘价买入涨跌幅
    df.loc[(df['trade_time'].notnull()) & (df['pos'] == 'buy'), 'strategy_pct'] = df['close'] / (
            df['open'] * (1 + trade_rate)) - 1

    df.loc[df['trade_time'].isnull() & (df['pos'] == 'buy'), 'strategy_pct'] = df['coin_pct']
    df.loc[df['trade_time'].isnull() & (df['pos'] == 'sell'), 'strategy_pct'] = 0
    df.loc[(df['trade_time'].notnull()) & (df['pos'] == 'sell'), 'strategy_pct'] = -trade_rate
    # # 扣除卖出手续费
    # df.loc[(df['trade_time'].shift(-1).notnull()), 'strategy_pct_adjust'] = (1 + df[
    #     'strategy_pct']) * (1 - trade_rate) - 1
    df['coin_net'] = (1 + df['coin_pct']).cumprod()
    df['strategy_net'] = (1 + df['strategy_pct']).cumprod()

    coin_net_ = df.loc[len(df) - 1, "coin_net"]
    strategy_net_ = df.loc[len(df) - 1, "strategy_net"]

    return coin_net_, strategy_net_


coin_list = ["BNB", "BTC", "DOT", "EOS", "ETH", "FIL", "LTC", "XRP"]
ma_list = [3, 5, 10, 20, 30, 50, 60, 90, 120, 240, 360]
mode_list = ["SMA", "EMA"]

fin_list = []
for coin_name in coin_list:
    for ma_len in ma_list:
        for mode_type in mode_list:
            coin_net, strategy_net = ema_test(coin_name_=coin_name, ma_len=ma_len, mode=mode_type)
            # print(coin_net, strategy_net)
            if coin_net != 0:
                res = [coin_name, ma_len, mode_type, coin_net, strategy_net, strategy_net > coin_net]
                fin_list.append(res)

res_df = pd.DataFrame(fin_list, columns=["币名", "周期", "周期线类型", "币自身回报", "策略回报", "策略是否跑赢大盘"])
res_df.to_csv("result/单均线策略测试.csv", encoding="gbk", index=False)
print(res_df)
