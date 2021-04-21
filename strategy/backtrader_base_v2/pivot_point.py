# -*- coding:utf-8 -*-
#
# Copyright (c) 2021 Hundsun.com, Inc. All Rights Reserved
#
"""
这个模块提供了

@FileName  :  pivot_point.py
@Author    :  yujl
@Time      :  2021/4/21 13:26
"""

import backtrader as bt

from strategy.backtrader_base_v2.background_logic import BasisStrategy

class PivotStrategy(BasisStrategy):
    def cal_technical_index(self):
        self.close = self.data.close

    def next(self):
        if self.order:
             return

        pre_high = self.data.high[-1]
        pre_low = self.data.low[-1]
        pre_close = self.data.close[-1]

        p_p = (pre_low + pre_high + pre_close) / 3.0
        p_r = 2 * p_p - pre_low
        p_s = 2 * p_p - pre_high

        if not self.position:
            if self.close[0] >= p_r:
                self.order = self.sell()
        else:
            if self.close[0] <= p_s:
                self.order = self.buy()

if __name__ == "__main__":
    pass
