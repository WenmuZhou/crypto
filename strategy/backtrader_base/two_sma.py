#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/4/21 9:26
# @Author   : Adolf
# @File     : two_sma.py
# @Function  :

import backtrader as bt
import pandas as pd

from strategy.backtrader_base.background_logic import BasisStrategy


class TwoSmaStrategy(BasisStrategy):
    """双均线策略
    《151 Trading Strategies》P50
    需要计算两类均值：短周期均值和长周期均值。当短周期均值穿过长周期均值买入，否则卖出
    Attributes:
        sma5: 短周期均值
        sma10: 长周期均值
    """
    params = (('short_period', 5), ('long_period', 10))

    def __init__(self):
        super(TwoSmaStrategy, self).__init__()

    @staticmethod
    def data_process(data_path):
        df = pd.read_csv(data_path)
        df["time_stamp"] = pd.to_datetime(df["time_stamp"])
        data = bt.feeds.PandasData(dataname=df, datetime="time_stamp", volume="vol")
        return data

    def cal_technical_index(self):
        self.sma_short = bt.indicators.MovingAverageSimple(self.datas[0], period=self.params.short_period)
        self.sma_long = bt.indicators.MovingAverageSimple(self.datas[0], period=self.params.long_period)

    def next(self):
        self.log('Close, %.2f' % self.data_close[0])

        if self.order:
            return

        if not self.position:
            if self.sma_short[0] > self.sma_long[0]:
                self.order = self.buy()
        else:
            if self.sma_short[0] < self.sma_long[0]:
                self.order = self.sell()


if __name__ == '__main__':
    TwoSmaStrategy.run(data_path="dataset/1d/BTC.csv", IS_All_IN=True, cash=10000000)

    '''
    cd /root/crypto && /root/anaconda3/envs/quant/bin/python -m trading.trade_execution.time_4h
    '''
