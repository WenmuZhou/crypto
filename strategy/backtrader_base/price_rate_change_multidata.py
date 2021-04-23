# -*- coding:utf-8 -*-
#
# Copyright (c) 2021 Hundsun.com, Inc. All Rights Reserved
#
"""
这个模块提供了

@FileName  :  price_rate_change_multidata.py
@Author    :  yujl
@Time      :  2021/4/23 15:22
"""

import pandas as pd
import backtrader as bt

from strategy.backtrader_base.background_logic import BasisStrategy


class PriceMomentumStrategyMultiData(BasisStrategy):
    params = (('timeperiod', 20),)

    def __init__(self):
        self.data_num = len(self.datas)
        super(PriceMomentumStrategyMultiData, self).__init__()

    def cal_technical_index(self):
        self.proc = {}
        for i in range(self.data_num):
            self.proc[i] = bt.talib.ROCP(self.datas[i].close, timeperiod=self.params.timeperiod)

    def prenext(self):
        print("prenext")
        dt = self.datas[0].datetime.date(-1)
        print('%s' % (dt.isoformat()))

    def nextstart(self):
        print("nextstart")
        dt = self.datas[0].datetime.date(-1)
        print('%s' % (dt.isoformat()))

    @staticmethod
    def data_process(data_paths):
        ret_datas = []
        for item in data_paths:
            df = pd.read_csv(item)
            df["time_stamp"] = pd.to_datetime(df["time_stamp"])
            data = bt.feeds.PandasData(dataname=df, datetime="time_stamp", volume="vol")
            ret_datas.append(data)
        return ret_datas

    def next(self):
        print("next")
        dt = self.datas[0].datetime.date(0)
        print('%s' % (dt.isoformat()))
        if self.order:
            return

        max_proc = -100
        max_index = -1
        for i in range(len(self.proc)):
            if self.proc[i][0] > max_proc:
                max_proc = self.proc[i][0]
                max_index = i
        print('==============')
        print(self.datas[0].datetime.date(0))
        print(max_index, max_proc)
        if not self.getposition(self.datas[max_index]) or max_index < 0:
            print(111111111111)
            for i in range(len(self.proc)):
                if self.getposition(self.datas[i]):
                    self.sell()

        if max_proc > 0:
            print(2222222222222)
            print(self.broker.getcash())
            print(self.datas[max_index].close[0])
            self.buy(data=self.datas[max_index], size=int(self.broker.getcash() / self.datas[max_index].close[0]))
            # self.buy(data=self.datas[max_index],size=10.3)

        # elif max_index != self.position:

        # for i in range(self.data_num):
        #     # print("i = {}, value = {}".format(i, self.proc[i][0]))
        #     if self.proc[i][0] < 0:
        #         self.order = self.sell(data=self.datas[i])
        #     else:
        #         if tmp_max < self.proc[i][0]:
        #             tmp_max = self.proc[i][0]
        #             tmp_idx = i
        # if tmp_idx >= 0:
        #     self.order = self.buy(data=self.datas[i])


if __name__ == "__main__":
    PriceMomentumStrategyMultiData.run(data_path=["dataset/1d/BTC.csv", "dataset/1d/ETH.csv"],
                                       cash=10000)
