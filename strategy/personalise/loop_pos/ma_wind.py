#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/5/24 15:59
# @Author   : Adolf
# @File     : ma_wind.py
# @Function  :
import pandas as pd
from strategy.personalise.loop_pos.base_structure import TradeStructure

pd.set_option("expand_frame_repr", False)
pd.set_option("display.max_rows", 1000)


class MaWind(TradeStructure):
    def __init__(self, data_path):
        super(MaWind, self).__init__(data_path)

    def cal_technical_index(self):
        self.data["MA5"] = self.data["close"].rolling(5).mean()
        self.data['MA10'] = self.data["close"].rolling(10).mean()

        self.data.loc[(self.data["MA5"] > self.data["MA10"]) & (
                self.data["MA5"].shift(1) < self.data["MA10"].shift(1)), "trade"] = "b"
        self.data.loc[(self.data["MA5"] < self.data["MA10"]) & (
                self.data["MA5"].shift(1) > self.data["MA10"].shift(1)), "trade"] = "s"

        self.data['diff'] = self.data["MA5"] - self.data["MA10"]
        self.data['diff'] = self.data['diff'].fillna(0)
        self.data["area"] = 0
        # print(self.data)

        area_ma = 0
        area_ma_list = []
        for index, row in self.data.iterrows():
            # print(row)
            self.data.loc[index, "area"] = area_ma
            if row["trade"] != "b" and row["trade"] != "s":
                area_ma += row["diff"]
            else:
                area_ma_list.append(area_ma)
                area_ma = row["diff"]

        # df2 = self.data[(self.data["trade"] == "s") | (self.data["trade"] == "b")]
        # df2.reset_index(inplace=True)
        # df2["pct"] = df2["close"].pct_change(periods=1).shift(-1)
        # df3 = df2[df2["trade"] == "b"]
        # print(df3)


if __name__ == '__main__':
    mawind = MaWind(data_path="dataset/stock/600570.csv")
    mawind.cal_technical_index()
