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

import pandas as pd
import backtrader as bt

import strategy_base

class SMAStrategy(strategy_base.BaseStrategy):

    def __init__(self):
        print("=======================")
        self.sma1 = bt.indicators.MovingAverageSimple(self.datas[0], period=5)
        self.sma2 = bt.indicators.MovingAverageSimple(self.datas[0], period=10)

        self.dataclose = self.datas[0].closez
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

    def run(self, df):
        self.process_data(df)
        self.cerebro.addstrategy(self)
        self.cerebro.broker.setcash(10000000)
        self.cerebro.broker.setcommission(commission=0.001)
        self.cerebro.broker.set_slippage_perc(0.001)
        self.cerebro.addsizer(bt.sizers.PercentSizer, percents=self.buy_percent)
        analyzers = {'sharp': bt.analyzers.SharpeRatio, 'annual_return': bt.analyzers.AnnualReturn,
         'drawdown': bt.analyzers.DrawDown}
        for name,ana_class in analyzers.items():
            self.cerebro.addanalyzer(ana_class, _name=name)
        back_rets = self.cerebro.run()

        return back_rets



if __name__ == "__main__":
    data_path = r'E:\\dataset\\day_stock_data\\sz.000338.csv'
    df = pd.read_csv(data_path)
    strategy_tester = SMAStrategy()
    strategy_tester.run(df)
