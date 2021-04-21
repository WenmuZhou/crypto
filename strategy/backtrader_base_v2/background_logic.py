#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/4/20 19:07
# @Author   : Adolf
# @File     : background_logic.py
# @Function  :
import backtrader as bt
import pandas as pd


class BasisStrategy(bt.Strategy):
    def log(self, txt, dt=None, doprint=False):
        if doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.data_close = self.datas[0].close
        self.order = None
        self.buy_price = None
        self.buy_comm = None

        self.cal_technical_index()

    def cal_technical_index(self):
        # self.sma5 = bt.indicators.MovingAverageSimple(self.datas[0], period=5)
        # self.sma10 = bt.indicators.MovingAverageSimple(self.datas[0], period=10)
        pass

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.buy_price = order.executed.price
                self.buy_comm = order.executed.comm
            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def next(self):
        pass

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm), doprint=True)

    def stop(self):
        self.log(u'Ending Value %.2f' %
                 (self.broker.getvalue()), doprint=True)

    @staticmethod
    def data_process(data_path):
        df = pd.read_csv(data_path)
        df["time_stamp"] = pd.to_datetime(df["time_stamp"])
        data = bt.feeds.PandasData(dataname=df,
                                   datetime="time_stamp",
                                   volume="vol")
        return data

    @classmethod
    def run(cls, data_path="", cash=100000, commission=0.0015):
        cerebro = bt.Cerebro()
        cerebro.addstrategy(cls)

        cerebro.adddata(cls.data_process(data_path))

        cerebro.broker.setcash(cash)
        cerebro.broker.setcommission(commission)

        cerebro.run()

# class BackTraderPipeline:
#     def __init__(self,
#                  data_path="",
#                  cash=10000,
#                  commission=0.0015,
#                  **kwargs):
#         self.data_path = data_path
#         self.cash = cash
#         self.commission = commission
#         self.cerebro = bt.Cerebro()
#
#     def data_process(self):
#         df = pd.read_csv(self.data_path)
#         df["time_stamp"] = pd.to_datetime(df["time_stamp"])
#         data = bt.feeds.PandasData(dataname=df,
#                                    datetime="time_stamp",
#                                    volume="vol")
#         return data
#
#     def __call__(self, MyStrategy):
#         self.cerebro.addstrategy(MyStrategy)
#
#         self.data_process()
#         self.cerebro.adddata(self.data_process())
#
#         self.cerebro.broker.setcash(self.cash)
#         self.cerebro.broker.setcommission(self.commission)
#
#         self.cerebro.run()
