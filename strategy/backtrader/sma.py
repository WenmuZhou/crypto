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

class SMAStrategy(bt.Strategy):
    params = (('period1', 5), ('period2', 10))

    def log(self, txt, dt=None, doprint=False):
        if doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.sma1 = bt.indicators.MovingAverageSimple(self.datas[0], period=self.p.peroid1)
        self.sma2 = bt.indicators.MovingAverageSimple(self.datas[0], period=self.p.peroid2)

        self.order = None
        self.buyprice = None
        self.buycomm = None
        self.dataclose = self.datas[0].close

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
            if self.sma1[0] > self.sma2[0]:
                self.order = self.buy(size=self.broker.getvalue() / self.dataclose)
        else:
            # 已经买了，如果 MA5 < MA10 ，说明跌势，卖出
            if self.sma1[0] < self.sma2[0]:
                self.order = self.sell()

    def stop(self):
        self.log(u'(金叉死叉有用吗) Ending Value %.2f' %
                 (self.broker.getvalue()), doprint=True)


if __name__ == "__main__":
    pass
