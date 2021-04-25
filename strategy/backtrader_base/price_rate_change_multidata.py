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
    params = (('timeperiod', 20),)

    def __init__(self):
        self.data_num = len(self.datas)
        super(PriceMomentumStrategyMultiData, self).__init__()

    def cal_technical_index(self):
        self.proc = {}
        for i in range(self.data_num):
            self.proc[i] = bt.talib.ROCP(self.datas[i].close, timeperiod=self.params.timeperiod)

    def prenext(self):
        # print("prenext")
        dt = self.datas[0].datetime.date(-1)
        # print('%s' % (dt.isoformat()))

    def nextstart(self):
        # print("nextstart")
        dt = self.datas[0].datetime.date(-1)
        # print('%s' % (dt.isoformat()))

    @staticmethod
    def data_process(data_paths):
        ret_datas = []
        for item in data_paths:
            df = pd.read_csv(item)
            df["time_stamp"] = pd.to_datetime(df["time_stamp"])
            data = bt.feeds.PandasData(dataname=df, datetime="time_stamp", volume="vol")
            ret_datas.append(data)
        return ret_datas

    def next(self):
        pass
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
        if not self.getposition(self.datas[max_index]) or max_index < 0:
            for i in range(len(self.proc)):
                if self.getposition(self.datas[i]):
                    self.order = self.sell(
                        size=self.position.size,
                    )

        if max_proc > 0:
            print('{} Send Buy, from data {}, open {}'.format(
                self.datas[max_index].datetime.date(),
                max_index,
                self.datas[max_index].open[0]
            ))
            self.order = self.buy(
                data=self.datas[max_index],
                size=(self.broker.getcash() / self.datas[max_index].open[0]),
            )
            # dt = self.datas[max_index].datetime.date(-1)
            # self.order = self.buy(data=self.datas[max_index],
            #                       size=(self.broker.getcash() / self.datas[max_index].open[0]))

if __name__ == "__main__":
    ret, cerebro = PriceMomentumStrategyMultiData.run(data_path=["dataset/1d/BTC.csv", "dataset/1d/ETH.csv"],
                                                cheat_on_open=True,
                                                cash=10000000,
                                                params_dict={'analyzers': {'sharp': bt.analyzers.SharpeRatio,
                                                                           'annual_return': bt.analyzers.AnnualReturn,
                                                                           'drawdown': bt.analyzers.DrawDown}}
                                                )

    print('Sharpe Ratio: ', ret[0].analyzers.sharp.get_analysis())
    print('annual return: ', ret[0].analyzers.annual_return.get_analysis())
    print('drawdown: ', ret[0].analyzers.drawdown.get_analysis())
    cerebro.plot(style='candle')

