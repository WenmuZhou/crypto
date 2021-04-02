#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/4/1 16:51
# @Author  : Adolf
# @File    : momentum_ma.py
import time
import talib
import pandas as pd

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

# print(df_eth)

df_btc_eth = pd.merge(left=df_btc[['time_stamp', 'btc_open', 'btc_close', 'btc_pct']], left_on=['time_stamp'],
                      right=df_eth[['time_stamp', 'eth_open', 'eth_close', 'eth_pct']], right_on=['time_stamp'],
                      how='left')

df = pd.merge(left=df_btc_eth[['time_stamp', 'btc_open', 'btc_close', 'btc_pct', 'eth_open', 'eth_close', 'eth_pct']],
              left_on=['time_stamp'],
              right=df_ltc[['time_stamp', 'ltc_open', 'ltc_close', 'ltc_pct']], right_on=['time_stamp'],
              how='left')

df['btc_30ma'] = talib.SMA(df['btc_close'], timeperiod=30)
df['eth_30ma'] = talib.SMA(df['eth_close'], timeperiod=30)
df['ltc_30ma'] = talib.SMA(df['ltc_close'], timeperiod=30)

df['btc_60ma'] = talib.SMA(df['btc_close'], timeperiod=60)
df['eth_60ma'] = talib.SMA(df['eth_close'], timeperiod=60)
df['ltc_60ma'] = talib.SMA(df['ltc_close'], timeperiod=60)

df['btc_mom'] = df['btc_close'].pct_change(periods=momentum_days)
df['eth_mom'] = df['eth_close'].pct_change(periods=momentum_days)
df['ltc_mom'] = df['ltc_close'].pct_change(periods=momentum_days)

df = df.dropna(how="any")
df.reset_index(drop=True, inplace=True)

print(df)
