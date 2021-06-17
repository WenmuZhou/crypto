 #!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/5/20 15:56
# @Author   : Adolf
# @File     : ma_mom.py
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
        def cal_vol_weight_ma(df, time_period):
            return df.apply(lambda row: row["close"] * row["volume"] , axis=1).rolling(
                time_period).mean() / df["volume"].rolling(time_period).mean()

        self.data["wma10"] = cal_vol_weight_ma(self.data, time_period=10)
        self.data["wma20"] = cal_vol_weight_ma(self.data, time_period=20)
        #
        self.data.dropna(how="any", inplace=True)

        self.data.loc[(self.data["wma10"] > self.data["wma20"]) & (
                self.data["wma10"].shift(1) <= self.data["wma20"].shift(1)), "trade"] = "buy"
        self.data.loc[(self.data["wma10"] < self.data["wma20"]) & (
                self.data["wma10"].shift(1) >= self.data["wma20"].shift(1)), "trade"] = "sell"
        # self.data.loc[(self.data["close"] > self.data["wma10"]) & (
        #         self.data["close"].shift(1) <= self.data["wma10"].shift(1)), "trade"] = "buy"
        # self.data.loc[(self.data["close"] < self.data["wma10"]) & (
        #         self.data["close"].shift(1) >= self.data["wma10"].shift(1)), "trade"] = "sell"
        print(self.data)


if __name__ == '__main__':
    mawind = MaWind(data_path="dataset/stock/600570_post.csv")
    # mawind.cal_technical_index()
    mawind(analyze_positions=True, make_plot_param={"is_make_plot": True})
