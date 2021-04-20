# -*- coding:utf-8 -*-
#
# Copyright (c) 2021 Hundsun.com, Inc. All Rights Reserved
#
"""
这个模块提供了

@FileName  :  data_base.py
@Author    :  yujl
@Time      :  2021/4/20 15:41
"""

import backtrader as bt

class BaseData(bt.feeds.PandasData):

    def data_process(self, df):
        df['date'] = pd.to_datetime(df['date'])
        data = bt.feeds.PandasData(
            dataname=df,
            # timeframe=self.time_frame,
            # fromdate=self.from_date,
            # todate=self.to_date,
            datetime='date',
            # open=self.open,
            # high=self.high,
            # low=self.low,
            # close=self.close,
            # volume=self.volume,
            # openinterest=self.openinterest,
        )
        return data

if __name__ == "__main__":
    pass
