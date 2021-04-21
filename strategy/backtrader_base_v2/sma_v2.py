#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/4/21 9:26
# @Author   : Adolf
# @File     : sma_v2.py
# @Function  :
from strategy.backtrader_base_v2.background_logic import BasisStrategy, BackTraderPipeline


class TestStrategy(BasisStrategy):
    def __init__(self):
        super(TestStrategy, self).__init__()

    def next(self):
        self.log('Close, %.2f' % self.data_close[0])

        if self.order:
            return

        if not self.position:
            if self.sma5[0] > self.sma10[0]:
                self.order = self.buy(size=self.broker.getvalue() / self.data_close)
        else:
            if self.sma5[0] < self.sma10[0]:
                self.order = self.sell()


if __name__ == '__main__':
    # MyPipeline = BackTraderPipeline(data_path="dataset/1d/BTC.csv")
    # MyPipeline(TestStrategy)
    TestStrategy.run(data_path="dataset/1d/BTC.csv")
