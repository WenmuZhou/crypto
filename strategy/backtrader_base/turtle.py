# -*- coding:utf-8 -*-
#
# Copyright (c) 2021 Hundsun.com, Inc. All Rights Reserved
#
"""
这个模块提供了简化海龟策略

@FileName  :  turtle.py
@Author    :  yujl
@Time      :  2021/4/21 11:25
"""

import backtrader as bt

from strategy.backtrader_base_v2.background_logic import BasisStrategy

class TurtleSizer(bt.Sizer):
    """交易量的大小

    计算每次交易多少
    每次买入时，买入的一个单元的股票

    Attributes:
        params: 设置单元大小
    """
    params = (('stake', 1),)

    def _getsizing(self, comminfo, cash, data, isbuy):
        if isbuy:
            return self.p.stake
        position = self.broker.getposition(data)
        if not position.size:
            return 0
        else:
            return position.size
        return self.p.stakeclass


class TurtleStrategy(BasisStrategy):
    """海龟交易策略
    https://www.definedge.com/turtle-trading-system/
    海龟交易策略最重要的是唐奇安通道
    唐奇安通道由两条线组成：
    上线：Max(最高价， n)
    下线：Min(最低价， n)
    穿越上线，买入；穿越下线，卖出

    Attributes:
        dataclose: 收盘价
        datahigh: 最高价
        datalow: 最低价
        buy_time: 买入次数
        buy_price: 买入价格
        Donchian_hi: 唐奇安通道上线
        Donchian_lo: 唐奇安通道下线
        TR: 真实波动
        ATR: 真实波动平均
        crossover_hi: 是否穿过上线
        crossover_lo: 是否穿过下线
    """
    def cal_technical_index(self):
        self.dataclose = self.datas[0].close
        self.datahigh = self.datas[0].high
        self.datalow = self.datas[0].low

        self.buy_time = 0
        self.buy_price = 0

        self.Donchian_hi = bt.indicators.Highest(self.datahigh(-1), period=20, subplot=False)
        self.Donchian_lo = bt.indicators.Lowest(self.datalow(-1), period=10, subplot=False)
        self.TR = bt.indicators.Max((self.datahigh(0) - self.datalow(0)), abs(self.dataclose(-1) - self.datahigh(0)),
                                    abs(self.dataclose(-1) - self.datalow(0)))
        self.ATR = bt.indicators.SimpleMovingAverage(self.TR, period=14, subplot=True)

        self.crossover_hi = bt.ind.CrossOver(self.dataclose(0), self.Donchian_hi)
        self.crossover_lo = bt.ind.CrossOver(self.dataclose(0), self.Donchian_lo)

    def next(self):
        if self.order:
            return
        #入场
        if self.crossover_hi > 0 and self.buy_time == 0:
            self.newstake = self.broker.getvalue() * 0.01 / self.ATR
            self.newstake = int(self.newstake / 100) * 100
            self.sizer.p.stake = self.newstake
            self.buy_time = 1
            self.order = self.buy()
        #加仓
        elif self.datas[0].close > self.buy_price + 0.5 * self.ATR[0] and self.buy_time > 0 and self.buy_time < 5:
            self.newstake = self.broker.getvalue() * 0.01 / self.ATR
            self.newstake = int(self.newstake / 100) * 100
            self.sizer.p.stake = self.newstake
            self.order = self.buy()
            self.buy_time = self.buy_time + 1
        #出场
        elif self.crossover_lo < 0 and self.buy_time > 0:
            self.order = self.sell()
            self.buy_time = 0
        #止损
        elif self.datas[0].close < (self.buy_price - 2 * self.ATR[0]) and self.buy_time > 0:
            self.order = self.sell()
            self.buy_time = 0


if __name__ == "__main__":
    pass
