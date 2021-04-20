# -*- coding:utf-8 -*-
#
# Copyright (c) 2021 Hundsun.com, Inc. All Rights Reserved
#
"""
这个模块提供了

@FileName  :  strategy_base.py
@Author    :  yujl
@Time      :  2021/4/20 10:05
"""

import pandas as pd
import backtrader as bt

import data_process

class BaseStrategy(bt.Strategy):
    """封装bt.Strategy类

    实现订单和交易的信息显示
    策略实现需要在子类的next方法中实现

    Attributes:
        order: 订单
        buy_price: 购买价
        buy_comm: 佣金
        bar_executed: 处理的数据个数
    """
    def log(self, txt, dt=None, do_print=False):
        if do_print:
            dt = dt or self.datas[0].datetime.date(0)
            print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.order = None
        self.buy_price = None
        self.buy_comm = None
        self.bar_executed = 0

        self.data_proc = data_process.DataProc()
        self.cerebro = bt.Cerebro()

    def next(self):
        pass

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
                self.buy_price = order.executed.price
                self.buy_comm = order.executed.comm
            self.bar_executed = len(self)

        # 订单因为缺少资金之类的原因被拒绝执行
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order status: {}, Canceled-{}/Margin-{}/Rejected-{}'.format(order.status, order.Canceled, order.Margin, order.Rejected), do_print=True)

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
                 (trade.pnl, trade.pnlcomm), do_print=True)

    def stop(self):
        self.log(u'Ending Value %.2f' %
                 (self.broker.getvalue()), do_print=True)

    def process_data(self, df):
        data = self.data_proc.data_process(df)
        self.cerebro.adddata(data)



if __name__ == "__main__":
    pass
