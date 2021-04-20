#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/4/6 10:26
# @Author  : Adolf
# @File    : bt_5_10.py
import backtrader as bt
import pandas as pd


# import os
# import sys
# import datetime


class TestStrategy(bt.Strategy):
    def log(self, txt, dt=None, doprint=False):
        if doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        self.buyprice = None
        self.buycomm = None

        self.sma5 = bt.indicators.MovingAverageSimple(self.datas[0], period=7)
        self.sma10 = bt.indicators.MovingAverageSimple(self.datas[0], period=25)

    def notify_order(self, order):
        """
        订单状态处理
        Arguments:
            order {object} -- 订单状态
        """
        if order.status in [order.Submitted, order.Accepted]:
            # 如订单已被处理，则不用做任何事情
            return

        # 检查订单是否完成
        if order.status in [order.Completed]:
            if order.isbuy():
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            self.bar_executed = len(self)

        # 订单因为缺少资金之类的原因被拒绝执行
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # 订单状态处理完成，设为空
        self.order = None

    def notify_trade(self, trade):
        """
        交易成果

        Arguments:
            trade {object} -- 交易状态
        """
        if not trade.isclosed:
            return

        # 显示交易的毛利率和净利润
        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm), doprint=True)

    def next(self):
        ''' 下一次执行 '''

        # 记录收盘价
        self.log('Close, %.2f' % self.dataclose[0])

        # 是否正在下单，如果是的话不能提交第二次订单
        if self.order:
            return

        # 是否已经买入
        if not self.position:
            # 还没买，如果 MA5 > MA10 说明涨势，买入
            if self.sma5[0] > self.sma10[0]:
                self.order = self.buy(size=self.broker.getvalue()/self.dataclose)
        else:
            # 已经买了，如果 MA5 < MA10 ，说明跌势，卖出
            if self.sma5[0] < self.sma10[0]:
                self.order = self.sell()

    def stop(self):
        self.log(u'(金叉死叉有用吗) Ending Value %.2f' %
                 (self.broker.getvalue()), doprint=True)


if __name__ == '__main__':
    # 初始化模型
    cerebro = bt.Cerebro()
    # 构建策略
    cerebro.addstrategy(TestStrategy)
    # 每次买100股
    # cerebro.addsizer(bt.sizers.FixedSize, stake=1)
    cerebro.addsizer(bt.sizers.PercentSizer, percents=100)

    df = pd.read_csv("dataset/1d/BTC.csv")
    df["time_stamp"] = pd.to_datetime(df["time_stamp"])
    # print(df)
    # exit()
    data = bt.feeds.PandasData(dataname=df, datetime="time_stamp",volume="vol")
    # 加载数据到模型中
    # data = bt.feeds.GenericCSVData(
    #     dataname='dataset/day/BTC.csv',
    #     fromdate=datetime.datetime(2018, 7, 4),
    #     todate=datetime.datetime(2021, 3, 28),
    #     dtformat='%Y-%m-%d',
    #     datetime=0,
    #     open=1,
    #     high=2,
    #     low=3,
    #     close=4,
    #     volume=5
    # )
    cerebro.adddata(data)

    # 设定初始资金和佣金
    cerebro.broker.setcash(30000.0)
    cerebro.broker.setcommission(0.001)

    # 策略执行前的资金
    print('启动资金: %.2f' % cerebro.broker.getvalue())

    # 策略执行
    cerebro.run()
