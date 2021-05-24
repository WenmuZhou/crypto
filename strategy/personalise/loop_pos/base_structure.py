#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/5/24 14:13
# @Author   : Adolf
# @File     : base_structure.py
# @Function  :
import pandas as pd


class TradeStructure:
    def __init__(self, data_path):
        self.position = self.init_position()
        self.data = self.load_dataset(data_path)
        self.trade_rate = 1 / 1000

    @staticmethod
    def init_position():
        return {
            "date": "",
            "pre_pos": 1,
            "pre_price": "cash",
            "pos_price": 1,
            "pos_style": "cash",
            "value": 1,
            "is_turn": False}

    @staticmethod
    def load_dataset(_data_path):
        df = pd.read_csv(_data_path)
        df = df[['date', 'open', 'close', 'high', 'low', 'volume']]
        df['trade'] = ""
        return df

    def cal_technical_index(self):
        self.data["MA5"] = self.data["close"].rolling(5).mean()
        self.data['MA10'] = self.data["close"].rolling(10).mean()

    def buy(self, buy_asset="stock", buy_price=1):
        self.position["pos_style"] = buy_asset
        self.position["pos_price"] = buy_price
        self.position['value'] *= (1 - self.trade_rate)

    def sell(self, sell_asset="stock", sell_price=1):
        self.position["pos_style"] = "cash"
        self.position["pos_price"] = 1
        self.position["value"] *= (1 + sell_price / self.position["pre_price"])
        self.position['value'] *= (1 - self.trade_rate)

    def strategy_exec(self):
        for index, row in self.data.iterrows():
            if row["trade"] == "buy":
                self.buy(buy_price=row["close"])
            if row["trade"] == "sell":
                self.sell(sell_price=row["close"])

    def __call__(self, show_buy_and_sell=False):
        self.cal_technical_index()
        if show_buy_and_sell:
            pass
        self.strategy_exec()
