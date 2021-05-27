#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/5/20 15:56
# @Author   : Adolf
# @File     : ma_mom.py
# @Function  :
import talib
import pandas as pd
import numpy as np
from strategy.personalise.loop_pos.base_structure import TradeStructure

pd.set_option("expand_frame_repr", False)
pd.set_option("display.max_rows", 1000)


class MaWind(TradeStructure):
    def cal_technical_index(self):
        self.data['wma5'] = (np.cumsum(self.data.volume * self.data.close) / np.cumsum(self.data.volume))

        # self.data["vol_w_ma5"] = cal_vol_weight_ma(self.data, time_period=5)
        # self.data["vol_w_ma10"] = cal_vol_weight_ma(self.data, time_period=10)
        #
        # self.data.loc[(self.data["vol_w_ma5"] > self.data["vol_w_ma10"]) & (
        #         self.data["vol_w_ma5"].shift(1) <= self.data["vol_w_ma10"].shift(1)), "trade"] = "buy"
        # self.data.loc[(self.data["vol_w_ma5"] < self.data["vol_w_ma10"]) & (
        #         self.data["vol_w_ma5"].shift(1) >= self.data["vol_w_ma10"].shift(1)), "trade"] = "sell"
        print(self.data)


if __name__ == '__main__':
    mawind = MaWind(data_path="dataset/stock/600570_post.csv")
    # mawind.cal_technical_index()
    mawind(analyze_positions=False, make_plot_param={"is_make_plot": True})
