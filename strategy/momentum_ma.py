#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/4/1 16:51
# @Author  : Adolf
# @File    : momentum_ma.py
import time
import pandas as pd
from backtest.base_function import evaluate_investment
import matplotlib.pyplot as plt

pd.set_option("expand_frame_repr", False)
pd.set_option("display.max_rows", 1000)

df_btc = pd.read_csv("dataset/day/BTC.csv")
df_eth = pd.read_csv("dataset/day/ETH.csv")
df_eos = pd.read_csv("dataset/day/EOS.csv")

trade_rate = 2 / 1000
# trade_rate = 0
momentum_days = 20

df_btc['btc_pct'] = df_btc['close'].pct_change(1)
df_eth['eth_pct'] = df_eth['close'].pct_change(1)
df_eos["eos_pct"] = df_eos['close'].pct_change(1)

df_btc.rename(columns={'open': 'btc_open', 'close': 'btc_close'}, inplace=True)
df_eth.rename(columns={'open': 'eth_open', 'close': 'eth_close'}, inplace=True)
df_eos.rename(columns={'open': 'eos_open', 'close': 'eos_close'}, inplace=True)

df1 = pd.merge(left=df_btc[['time_stamp', 'btc_open', 'btc_close', 'btc_pct']], left_on=['time_stamp'],
             right=df_eth[['time_stamp', 'eth_open', 'eth_close', 'eth_pct']], right_on=['time_stamp'],
              how='left')

df2 = pd.merge(le)
# print(df_coin1)
