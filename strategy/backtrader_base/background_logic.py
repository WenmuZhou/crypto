#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/4/20 19:07
# @Author   : Adolf
# @File     : background_logic.py
# @Function  :
import backtrader as bt
import pandas as pd


class CommInforFractional(bt.CommissionInfo):
    def getsize(self, price, cash):
        return self.p.leverage * (cash / price)


class BasisStrategy(bt.Strategy):
    cls_ret = {}

    def log(self, txt, dt=None, doprint=True):
        if doprint:
            dt = dt or self.datas[0].datetime.datetime(0)
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

    def next(self):
        pass

    def notify_order(self, order):
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
            # print(self.datas)
            self.log(
                'Order status: {}, Canceled-{}/Margin-{}/Rejected-{}'.format(order.status, order.Canceled, order.Margin,
                                                                             order.Rejected), doprint=True)

        self.log('Value: {:.6f}, price: {:.6f}, size: {}'.format(order.executed.value, order.executed.price,
                                                                 order.executed.size), doprint=True)
        # 订单状态处理完成，设为空
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm), doprint=False)

    def stop(self):
        self.log(u'Ending Value %.2f' %
                 (self.broker.getvalue()), doprint=False)
        for i in range(len(self.datas)):
            self.log('coin name:{},coin yield:{:.2f}'.
                     format(i, self.datas[i].close[0] / self.datas[i].close[-len(self.datas[i]) + 1]), doprint=False)
        self.log('strategy yield:{:.2f}'.format(self.broker.getvalue() / self.origin_cash), doprint=False)
        BasisStrategy.cls_ret = {}
        for i in range(len(self.datas)):
            BasisStrategy.cls_ret['coin_yield_{}'.format(i)] = self.datas[i].close[0] / self.datas[i].close[
                -len(self.datas[i]) + 1]

        BasisStrategy.cls_ret['strategy_yield'] = self.broker.getvalue() / self.origin_cash
        BasisStrategy.cls_ret['end_value'] = self.broker.get_value()

    @staticmethod
    def data_process(data_path):
        df = pd.read_csv(data_path)
        df["date"] = pd.to_datetime(df["date"])
        data = bt.feeds.PandasData(dataname=df,
                                   datetime="date",
                                   volume="volume")
        return data

    @classmethod
    def run(cls, data_path="", cash=100000, commission=1 / 1000, slip_type=-1, slip_value=0, IS_ALL_IN=False,
            params_dict={}, make_plot=False):
        cls.origin_cash = cash
        strategy_params = params_dict.get("strategy_params", {})
        analyzer_params = params_dict.get('analyzers', {})
        plot_params = params_dict.get("plot", {})

        cerebro = bt.Cerebro(cheat_on_open=IS_ALL_IN)
        cerebro.addstrategy(cls, **strategy_params)
        datas = cls.data_process(data_path)
        if isinstance(datas, list):
            for item in datas:
                cerebro.adddata(item)
        else:
            cerebro.adddata(datas)

        cerebro.broker.setcash(cash)
        cerebro.broker.setcommission(commission)  # (commission)

        cerebro.broker.addcommissioninfo(CommInforFractional())
        # 滑点、投入资金百分比、回测指标
        # 按照固定值设置滑点
        if slip_type == 0:
            cerebro.broker.set_slippage_fixed(slip_value)
        # 按照百分比设置滑点
        elif slip_type == 1:
            cerebro.broker.set_slippage_perc(slip_value)

        for ana_name, ana_class in analyzer_params.items():
            cerebro.addanalyzer(ana_class, _name=ana_name)

        back_ret = cerebro.run()
        if make_plot:
            cerebro.plot(**plot_params)
        return back_ret, cerebro, cls.cls_ret
