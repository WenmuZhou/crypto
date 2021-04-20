# -*- coding:utf-8 -*-
#
# Copyright (c) 2021 Hundsun.com, Inc. All Rights Reserved
#
"""
这个模块提供了

@FileName  :  ketler.py
@Author    :  yujl
@Time      :  2021/4/20 15:05
"""

import backtrader as bt

import strategy_base

class KetlerStrategy(strategy_base.BaseStrategy):
    def __init__(self):
        self.expo = bt.talib.EMA(self.datas[0].close, timeperiod=20)
        self.atr = bt.talib.ATR(self.data.high, self.data.low, self.data.close, timeperiod=17)
        self.upper = self.expo + self.atr
        self.lower = self.expo - self.atr

        self.dataclose = self.datas[0].close
        super(KetlerStrategy, self).__init__()

    def next(self):
        """策略核心，策略执行流程"""

        # 如果已经下单，则返回
        if self.order:
            return

        # 是否已买入
        if not self.position:
            # 没有买入，如果收盘价>上线，表示股票涨势，买入
            if self.close[0] > self.upper[0]:
                self.order = self.order_target_percent(target=0.95)
        else:
            # 已经买了，如果收盘价<中线，表示股票跌势，卖出
            if self.close[0] < self.expo[0]:
                self.order = self.sell()

if __name__ == "__main__":
    pass
