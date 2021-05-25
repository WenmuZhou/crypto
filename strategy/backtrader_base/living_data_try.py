# -*- coding:utf-8 -*-
#
# Copyright (c) 2021 Hundsun.com, Inc. All Rights Reserved
#
"""
这个模块提供了

@FileName  :  living_data_try.py
@Author    :  yujl
@Time      :  2021/5/25 14:18
"""

import time
import datetime

import backtrader as bt
import pandas as pd

class LivingData(bt.feed.DataBase):
    params = (
        ('sleeptime', 5),
        ('csv_path', None),
    )
    def __init__(self, symbol, **kwargs):
        super().__init__(**kwargs)
        self.symbol = symbol
        self.last_dt = datetime.datetime.now()
        self.df = pd.read_csv(self.p.csv_path)
        self.df_len = len(self.df)
        # self.df_len = 10
        self.counter = 0
        print("All number is {}".format(self.df_len))

    def start(self):
        super().start()
        self.resample(timeframe=self.p.timeframe, compression=self.p.compression)

    def stop(self):
        pass

    def islive(self):
        return True

    def _load(self):
        msg = self._req_data()
        if msg is None:
            return False

        self.lines.datetime[0] = self.date2num(msg['datetime'])
        self.lines.open[0] = msg['open']
        self.lines.high[0] = msg['high']
        self.lines.low[0] = msg['low']
        self.lines.close[0] = msg['close']
        self.lines.volume[0] = msg['volume']

        return True

    def _req_data(self):
        time.sleep(self.p.sleeptime)
        msg = dict()

        if self.counter >= self.df_len:
            return None
        else:
            data = self.df.loc[self.counter]
            msg['datetime'] = datetime.datetime.strptime(data[0], '%Y-%m-%d').date()
            msg['open'] = float(data[1])
            msg['high'] = float(data[2])
            msg['low'] = float(data[3])
            msg['close'] = float(data[4])
            msg['volume'] = int(data[5])
            self.counter += 1
            # print(msg)
        return msg

class TestStrategy(bt.Strategy):
    params = (('period', 5), )

    def __init__(self):
        self.kama = bt.talib.SMA(self.data0.close, timeperiod=self.params.period)

    def prenext(self):
        print('prenext: close:{}, open:{}, kama:{}'.format(self.data0.close[0], self.data0.open[0], self.kama[0]))

    def next(self):
        print('next: close:{}, open:{}, kama:{}'.format(self.data0.close[0], self.data0.open[0], self.kama[0]))


if __name__ == "__main__":
    cerebro = bt.Cerebro()
    cerebro.addstrategy(TestStrategy)
    feed = LivingData('ixic', timeframe=bt.TimeFrame.Days, compression=1, csv_path='dataset/stock/000333.csv')
    cerebro.adddata(feed, name='living_try')

    result = cerebro.run()


    # df = pd.read_csv('dataset/stock/000333.csv')
    # df_len = len(df)
    # print(df_len)
    # print(df.loc[0])
    # print(type(df.loc[0]))
    # data = df.loc[0]
    # print(data[0])
    # print(data[1])
    # print(type(data[1]))
    # print(type(float(data[1])))
    # print(type(data[0]))

