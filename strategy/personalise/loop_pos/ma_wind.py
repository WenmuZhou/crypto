#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/5/24 15:59
# @Author   : Adolf
# @File     : ma_wind.py
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
        self.data["ma5"] = self.data["close"].rolling(5).mean()
        self.data['ma10'] = self.data["close"].rolling(10).mean()

        self.data.loc[(self.data["ma5"] > self.data["ma10"]) & (
                self.data["ma5"].shift(1) <= self.data["ma10"].shift(1)), "trade"] = "buy"
        self.data.loc[(self.data["ma5"] < self.data["ma10"]) & (
                self.data["ma5"].shift(1) >= self.data["ma10"].shift(1)), "trade"] = "sell"

        # 计算MACD指标
        self.data['MACD'], self.data['MACDsignal'], self.data['MACDhist'] = talib.MACD(self.data.close, fastperiod=12,
                                                                                       slowperiod=26,
                                                                                       signalperiod=9)

        # 计算KDJ指标
        self.data['slowk'], self.data['slowd'] = talib.STOCH(
            self.data['high'].values,
            self.data['low'].values,
            self.data['close'].values,
            fastk_period=9,
            slowk_period=3,
            slowk_matype=0,
            slowd_period=3,
            slowd_matype=0)
        # 求出J值，J = (3*K)-(2*D)
        self.data['slowj'] = list(map(lambda x, y: 3 * x - 2 * y, self.data['slowk'], self.data['slowd']))

        self.data.fillna(0, inplace=True)
        # print(self.data)

        # print(self.data)
        # self.data['diff'] = self.data.apply(lambda x: (x.ma5 - x.ma10) / min(x.ma5, x.ma10), axis=1)
        # self.data["area"] = 0
        # area_ma = 0
        # area_ma_list = []
        # for index, row in self.data.iterrows():
        #     # print(row)
        #     self.data.loc[index, "area"] = area_ma
        #     if row["trade"] != "buy" and row["trade"] != "sell":
        #         area_ma += row["diff"]
        #     else:
        #         area_ma_list.append(area_ma)
        #         area_ma = row["diff"]
        # df2 = self.data[(self.data["trade"] == "sell") | (self.data["trade"] == "buy")].copy()
        # df2.reset_index(inplace=True)
        # df2["pct"] = df2["close"].pct_change(periods=1).shift(-1)
        # df3 = df2[df2["trade"] == "b"].copy()
        # print(df3)
        # df4 = df3[abs(df3["area"]) < 0.2].copy()
        # df3['origin_pct'] = (1 + df3['pct']).cumprod()
        # df4['adjust_pct'] = (1 + df4['pct']).cumprod()
        # print(df3.tail(2)["origin_pct"])
        # print('------')
        # print(df4.tail(2)["adjust_pct"])


if __name__ == '__main__':
    mawind = MaWind(data_path="dataset/stock/600570_post.csv")
    mawind.cal_technical_index()
    # mawind(analyze_positions=True)
