# -*- coding:utf-8 -*-
#
# Copyright (c) 2021 Hundsun.com, Inc. All Rights Reserved
#
"""
这个模块提供了

@FileName  :  sma.py
@Author    :  yujl
@Time      :  2021/4/20 8:41
"""

import backtrader as bt

import strategy_base

class SMAStrategy(strategy_base.BaseStrategy):

    def __init__(self):
        self.sma1 = bt.indicators.MovingAverageSimple(self.datas[0], period=5)
        self.sma2 = bt.indicators.MovingAverageSimple(self.datas[0], period=10)

        self.dataclose = self.datas[0].close
        super(SMAStrategy, self).__init__()

    def next(self):
        ''' 执行策略 '''

        # 记录收盘价
        self.log('Close, %.2f' % self.dataclose[0])

        # 是否正在下单，如果是的话不能提交第二次订单
        if self.order:
            return

        # 是否已经买入
        if not self.position:
            # 还没买，如果 MA5 > MA10 说明涨势，买入
            if self.sma1[0] > self.sma2[0]:
                self.order = self.buy()
        else:
            # 已经买了，如果 MA5 < MA10 ，说明跌势，卖出
            if self.sma1[0] < self.sma2[0]:
                self.order = self.sell()




if __name__ == "__main__":
    pass
