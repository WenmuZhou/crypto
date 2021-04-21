#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/4/21 9:26
# @Author   : Adolf
# @File     : sma_v2.py
# @Function  :

import backtrader as bt

from strategy.backtrader_base_v2.background_logic import BasisStrategy

class TestStrategy(BasisStrategy):
    """双均线策略
    《151 Trading Strategies》P50
    需要计算两类均值：短周期均值和长周期均值。当短周期均值穿过长周期均值买入，否则卖出
    Attributes:
        sma5: 短周期均值
        sma10: 长周期均值
    """
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
