#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/6/17 9:33
# @Author   : Adolf
# @File     : ths_ls.py
# @Function  :
import pandas
import talib
import pandas as pd
import numpy as np
from strategy.personalise.loop_pos.base_structure import TradeStructure

pd.set_option("expand_frame_repr", False)
pd.set_option("display.max_rows", 1000)


class MaWind(TradeStructure):
    def cal_technical_index(self):
        self.data['var1'] = (100 - (90 * (self.data.high.rolling(21).max() - self.data.close) / (self.data.high.rolling(
            21).max() - self.data.low.rolling(21).min())))
        self.data["var2"] = self.data["var1"]
        self.data["var3_tmp"] = 100 * (self.data.high.rolling(6).max() - self.data.close) / (self.data.high.rolling(
            6).max() - self.data.low.rolling(6).min())
        self.data["var3"] = 100 - self.data.var3_tmp.rolling(34).mean()

        self.data["var4"] = self.data.var3.rolling(6).mean()

        self.data.loc[(self.data["var2"] > self.data["var4"]) & (
                self.data["var2"].shift(1) <= self.data["var4"].shift(1)), "trade"] = "buy"
        self.data.loc[(self.data["var2"] < self.data["var4"]) & (
                self.data["var2"].shift(1) >= self.data["var4"].shift(1)), "trade"] = "sell"

        del self.data["var1"], self.data["var2"], self.data["var3_tmp"], self.data["var3"], self.data["var4"]
        self.data.dropna(inplace=True)
        self.data = self.data[-2000:]
        # print(self.data.tail(100))


if __name__ == '__main__':
    mawind = MaWind(data_path="/data3/stock_data/stock_data/real_data/bs/post_d/sh.600570.csv")
    # mawind.cal_technical_index()
    mawind(analyze_positions=True, make_plot_param={"is_make_plot": False})
