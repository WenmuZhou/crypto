# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @Project : crypto
# @Date    : 2021/4/18 21:56
# @Author  : Adolf
# @File    : base_strategy.py
# @Function:
import pandas as pd
import numpy as np


class BasisStrategy:
    def __init__(self, coin_list, trade_rate=1.5 / 1000):
        self.coin_list = coin_list
        self.trade_rate = trade_rate

    def cal_transaction_fees(self, df):
        df.loc[(df['trade_time'].notnull()) & (df['pos'] == 'coin1'), 'strategy_pct_adjust'] = df['coin1_close'] / (
                df['coin1_open'] * (1 + self.trade_rate)) - 1
        df.loc[(df['trade_time'].notnull()) & (df['pos'] == 'coin2'), 'strategy_pct_adjust'] = df['coin2_close'] / (
                df['coin2_open'] * (1 + self.trade_rate)) - 1
        df.loc[df['trade_time'].isnull(), 'strategy_pct_adjust'] = df['strategy_pct']
        df.loc[(df['trade_time'].shift(-1).notnull()) & (df["pos"] != "empty"), 'strategy_pct'] = \
            (1 + df['strategy_pct']) * (1 - df) - 1
        df.reset_index(drop=True, inplace=True)

    def main(self):
        pass