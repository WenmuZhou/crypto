#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/5/31 17:30
# @Author   : Adolf
# @File     : chan_ma.py
# @Function  :
import talib
import pandas as pd
from strategy.personalise.loop_pos.base_structure import TradeStructure

pd.set_option("expand_frame_repr", False)
pd.set_option("display.max_rows", 1000)


class MaWind(TradeStructure):
    def __init__(self, data_path):
        super(MaWind, self).__init__(data_path)

    def cal_technical_index(self):
        self.data = self.data[:100]
        self.data["ma5"] = self.data["close"].rolling(5).mean()
        self.data['ma10'] = self.data["close"].rolling(10).mean()

        self.data.loc[(self.data["ma5"] > self.data["ma10"]) & (
                self.data["ma5"].shift(1) <= self.data["ma10"].shift(1)), "trade"] = "buy"
        self.data.loc[(self.data["ma5"] < self.data["ma10"]) & (
                self.data["ma5"].shift(1) >= self.data["ma10"].shift(1)), "trade"] = "sell"

        print(self.data)


if __name__ == '__main__':
    mawind = MaWind(data_path="dataset/stock/600570_post.csv")
    mawind.cal_technical_index()
    # mawind(analyze_positions=True)
