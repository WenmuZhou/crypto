# -*- coding:utf-8 -*-
#
# Copyright (c) 2021 Hundsun.com, Inc. All Rights Reserved
#
"""
这个模块提供了

@FileName  :  ketler_v2.py
@Author    :  yujl
@Time      :  2021/4/21 10:37
"""

from strategy.backtrader_base.background_logic import BasisStrategy
import backtrader as bt

class KetlerStrategy(BasisStrategy):
    def cal_technical_index(self):
        self.expo = bt.talib.EMA(self.datas[0].close, timeperiod=20)
        self.atr = bt.talib.ATR(self.data.high, self.data.low, self.data.close, timeperiod=17)
        self.upper = self.expo + self.atr
        self.lower = self.expo - self.atr

    def next(self):
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
    # KetlerStrategy.run(data_path=r"F:\\stock_data\hs300_d\\sz.000001.csv")
    pass
