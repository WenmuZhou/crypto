#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/4/21 9:26
# @Author   : Adolf
# @File     : sma_v2.py
# @Function  :
from strategy.backtrader_base.background_logic import BasisStrategy
import backtrader as bt


class TestStrategy(BasisStrategy):
    def cal_technical_index(self):
        self.sma5 = bt.indicators.MovingAverageSimple(self.datas[0], period=5)
        self.sma10 = bt.indicators.MovingAverageSimple(self.datas[0], period=10)

    def next(self):
        self.log('Close, %.2f' % self.data_close[0])

        if self.order:
            return

        if not self.position:
            if self.sma5[0] > self.sma10[0]:
                self.order = self.buy()
        else:
            if self.sma5[0] < self.sma10[0]:
                self.order = self.sell()


if __name__ == '__main__':
    TestStrategy.run(data_path=r"F:\\stock_data\hs300_d\\sz.000001.csv")
