# -*- coding:utf-8 -*-
#
# Copyright (c) 2021 Hundsun.com, Inc. All Rights Reserved
#
"""
这个模块提供了

@FileName  :  price_rate_change_multidata.py
@Author    :  yujl
@Time      :  2021/4/23 15:22
"""

import pandas as pd
import backtrader as bt

from strategy.backtrader_base.background_logic import BasisStrategy


class PriceMomentumStrategyMultiData(BasisStrategy):
    params = (('time_period', 20),)

    def __init__(self):
        self.data_num = len(self.datas)
        super(PriceMomentumStrategyMultiData, self).__init__()

    def cal_technical_index(self):
        self.proc = {}
        for i in range(self.data_num):
            self.proc[i] = bt.talib.ROCP(self.datas[i].close, timeperiod=self.params.time_period)

    def prenext(self):
        dt = self.datas[0].datetime.date(-1)

    def nextstart(self):
        dt = self.datas[0].datetime.date(-1)

    @staticmethod
    def data_process(data_paths):
        ret_datas = []
        for item in data_paths:
            df = pd.read_csv(item)
            df["time_stamp"] = pd.to_datetime(df["time_stamp"])
            data = bt.feeds.PandasData(dataname=df, datetime="time_stamp", volume="vol")
            ret_datas.append(data)
        return ret_datas

    # def next(self):
    # if self.order:
    #     return
    #
    # max_proc = -100
    # max_index = -1
    # for i in range(len(self.proc)):
    #     if self.proc[i][0] > max_proc:
    #         max_proc = self.proc[i][0]
    #         max_index = i
    # if not self.getposition(self.datas[max_index]) or max_index < 0:
    #     for i in range(len(self.proc)):
    #         if self.getposition(self.datas[i]):
    #             self.order = self.sell()
    #
    # if max_proc > 0:
    #     print('{} Send Buy, from data {}, open {}'.format(
    #         self.datas[max_index].datetime.date(),
    #         max_index,
    #         self.datas[max_index].open[0]
    #     ))
    #     self.order = self.buy()
    #
    # print('Value: {:.2f}, price: {:.2f}, size: {:.2f}'.format(self.order.executed.value, self.order.executed.price, self.order.executed.size))
    # dt = self.datas[max_index].datetime.date(-1)
    # print('%s' % (dt.isoformat()))
    # self.order = self.buy(data=self.datas[max_index],
    #                       size=(self.broker.getcash() / self.datas[max_index].open[0]))

    # self.order = self.buy(data=self.datas[max_index],
    #                       size=int(self.broker.getcash() / self.datas[max_index].close[0]),
    #                       price=self.datas[max_index].close[0])

    def next_open(self):
        if self.order:
            return

        max_proc = -100
        max_index = -1
        for i in range(len(self.proc)):
            if self.proc[i][0] > max_proc:
                max_proc = self.proc[i][0]
                max_index = i
        # print('111111', self.position)
        if not self.getposition(self.datas[max_index]) or max_index < 0:
            for i in range(len(self.proc)):
                if self.getposition(self.datas[i]):
                    # print("xxxxxxxxxxxx")
                    self.order = self.sell(
                        size=-self.position.size,
                        data=self.datas[i],
                    )
        # print('222222', self.position)
        if max_proc > 0:
            # print('{} Send Buy, from data {}, open {}'.format(
            #     self.datas[max_index].datetime.date(),
            #     max_index,
            #     self.datas[max_index].open[0]
            # ))
            self.order = self.buy(
                data=self.datas[max_index],
                size=(self.broker.getcash() / self.datas[max_index].open[0]),
            )
            # dt = self.datas[max_index].datetime.date(-1)
            # self.order = self.buy(data=self.datas[max_index],
            #                       size=(self.broker.getcash() / self.datas[max_index].open[0]))


if __name__ == "__main__":
    for i in range(3, 200):
        print("time_period:", i)
        ret, cerebro = PriceMomentumStrategyMultiData.run(
            data_path=["dataset/1d/BTC.csv", "dataset/1d/ETH.csv", "dataset/1d/ADA.csv", "dataset/1d/BNB.csv",
                       "dataset/1d/DOT.csv", "dataset/1d/UNI.csv", ],
            IS_ALL_IN=True,
            cash=10000000,
            params_dict={"strategy_params":
                             {"time_period": i, },
                         'analyzers': {
                             'sharp': bt.analyzers.SharpeRatio,
                             'annual_return': bt.analyzers.AnnualReturn,
                             'drawdown': bt.analyzers.DrawDown}}
        )

        # print('Sharpe Ratio: ', ret[0].analyzers.sharp.get_analysis()["sharperatio"])
        # print('annual return: ', ret[0].analyzers.annual_return.get_analysis())
        print('drawdown: ', ret[0].analyzers.drawdown.get_analysis()["max"]["drawdown"])
        print('-' * 200)
        # break
    # cerebro.plot(style='candle')
