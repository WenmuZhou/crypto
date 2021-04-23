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
    params = (('timeperiod', 14), )

    def __init__(self):
        self.data_num = len(self.datas)
        print(self.data_num)
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
            df["date"] = pd.to_datetime(df["date"])
            data = bt.feeds.PandasData(dataname=df, datetime="date", volume="volume")
            ret_datas.append(data)
        return ret_datas

    def next(self):
        # dt = self.datas[0].datetime.date(0)
        # print('%s' % (dt.isoformat()))
        if self.order:
            return

        tmp_max = 0
        tmp_idx = -1
        for i in range(self.data_num):
            # print("i = {}, value = {}".format(i, self.proc[i][0]))
            if self.proc[i][0] < 0:
                self.order = self.sell(data=self.datas[i])
            else:
                if tmp_max < self.proc[i][0]:
                    tmp_max = self.proc[i][0]
                    tmp_idx = i
        if tmp_idx >= 0:
            self.order = self.buy(data=self.datas[i])



if __name__ == "__main__":
    pass
