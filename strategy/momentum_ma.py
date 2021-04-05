#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/4/1 16:51
# @Author  : Adolf
# @File    : momentum_ma.py
import time
import numpy as np
import pandas as pd
import talib

pd.set_option("expand_frame_repr", False)
pd.set_option("display.max_rows", 1000)

df_btc = pd.read_csv("dataset/day/BTC.csv")
df_eth = pd.read_csv("dataset/day/ETH.csv")
df_ltc = pd.read_csv("dataset/day/LTC.csv")

trade_rate = 2 / 1000
# trade_rate = 0
momentum_days = 20

df_btc['btc_pct'] = df_btc['close'].pct_change(1)
df_eth['eth_pct'] = df_eth['close'].pct_change(1)
df_ltc["ltc_pct"] = df_ltc['close'].pct_change(1)

df_btc.rename(columns={'open': 'btc_open', 'close': 'btc_close'}, inplace=True)
df_eth.rename(columns={'open': 'eth_open', 'close': 'eth_close'}, inplace=True)
df_ltc.rename(columns={'open': 'ltc_open', 'close': 'ltc_close'}, inplace=True)

df_btc_eth = pd.merge(left=df_btc[['time_stamp', 'btc_open', 'btc_close', 'btc_pct']], left_on=['time_stamp'],
                      right=df_eth[['time_stamp', 'eth_open', 'eth_close', 'eth_pct']], right_on=['time_stamp'],
                      how='left')

df = pd.merge(left=df_btc_eth[['time_stamp', 'btc_open', 'btc_close', 'btc_pct', 'eth_open', 'eth_close', 'eth_pct']],
              left_on=['time_stamp'],
              right=df_ltc[['time_stamp', 'ltc_open', 'ltc_close', 'ltc_pct']], right_on=['time_stamp'],
              how='left')

df['btc_mom'] = df['btc_close'].pct_change(periods=momentum_days)
df['eth_mom'] = df['eth_close'].pct_change(periods=momentum_days)
df['ltc_mom'] = df['ltc_close'].pct_change(periods=momentum_days)

df["btc_30_ma"] = talib.SMA(df['btc_close'], timeperiod=30)
df["eth_30_ma"] = talib.SMA(df['eth_close'], timeperiod=30)
df["ltc_30_ma"] = talib.SMA(df['ltc_close'], timeperiod=30)

df["btc_60_ma"] = talib.SMA(df['btc_close'], timeperiod=60)
df["eth_60_ma"] = talib.SMA(df['eth_close'], timeperiod=60)
df["ltc_60_ma"] = talib.SMA(df['ltc_close'], timeperiod=60)

df = df.dropna(how="any")
df.reset_index(drop=True, inplace=True)

df.loc[df["btc_close"] > df["btc_30_ma"], "btc_30_bull"] = 1
df.loc[df["eth_close"] > df["eth_30_ma"], "eth_30_bull"] = 1
df.loc[df["ltc_close"] > df["ltc_30_ma"], "ltc_30_bull"] = 1

df.loc[df["btc_close"] > df["btc_60_ma"], "btc_60_bull"] = 1
df.loc[df["eth_close"] > df["eth_60_ma"], "eth_60_bull"] = 1
df.loc[df["ltc_close"] > df["ltc_60_ma"], "ltc_60_bull"] = 1

df = df.fillna(0)
df.loc[sum([df["btc_30_bull"], df["eth_30_bull"], df["ltc_30_bull"]]) > 1, "market_30_bull"] = 1
df.loc[sum([df["btc_60_bull"], df["eth_60_bull"], df["ltc_60_bull"]]) > 1, "market_60_bull"] = 1
df = df.fillna(0)
print(df)

df.loc[max(enumerate([df["btc_30_mom"], df["eth_30_mom"], df["ltc_30_mom"]]), key=lambda x: x[1])[0], 'style'] = 'coin1'
df.loc[(df['coin1_mom'] < 0) & (df['coin2_mom'] < 0), 'style'] = 'empty'

df['style'].fillna(method='ffill', inplace=True)
# 收盘才能确定风格，实际的持仓pos要晚一天。
df['pos'] = df['style'].shift(1)
# 删除持仓为nan的天数
df.dropna(subset=['pos'], inplace=True)

df.loc[df['pos'] == 'coin1', 'strategy_pct'] = df['coin1_pct']
df.loc[df['pos'] == 'coin2', 'strategy_pct'] = df['coin2_pct']
# print(df_coin1)
