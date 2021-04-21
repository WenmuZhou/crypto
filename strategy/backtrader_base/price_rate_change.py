# -*- coding:utf-8 -*-
#
# Copyright (c) 2021 Hundsun.com, Inc. All Rights Reserved
#
"""
这个模块提供了

@FileName  :  price_rate_change.py
@Author    :  yujl
@Time      :  2021/4/21 13:13
"""
import pandas as pd
import backtrader as bt

from strategy.backtrader_base.background_logic import BasisStrategy


class PriceMomentumStrategy(BasisStrategy):
    def cal_technical_index(self):

        self.proc = bt.talib.ROCP(self.datas[0].close, timeperiod=14)

    @staticmethod
    def data_process(data_path):
        df = pd.read_csv("dataset/1d/BTC.csv")
        df["time_stamp"] = pd.to_datetime(df["time_stamp"])
        data = bt.feeds.PandasData(dataname=df, datetime="time_stamp", volume="vol")
        return data

    def next(self):
        if self.order:
            return
        if not self.position:
            # 没有买入，如果价格动量大于零，表示股票涨势，买入
            if self.proc[0] > 0:
                self.order = self.buy()  # (target=0.90)
        else:
            # 已经买入，如果价格动量小于零，表示股票跌势，卖出
            if self.proc[0] < 0:
                self.order = self.sell()


if __name__ == "__main__":
    PriceMomentumStrategy.run(data_path="dataset/1d/BTC.csv")
