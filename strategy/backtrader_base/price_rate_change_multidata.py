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
import datetime

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

    # def prenext(self):
    #     dt = self.datas[0].datetime.date(-1)

    # def prenext_open(self):
    #     dt = self.datas[0].datetime.date(-1)
    #
    # def nextstart_open(self):
    #     dt = self.datas[0].datetime.date(-1)

    # def nextstart(self):
    #     dt = self.datas[0].datetime.date(-1)

    @staticmethod
    def data_process(data_paths):
        ret_datas = []
        for item in data_paths:
            df = pd.read_csv(item)
            df["date"] = pd.to_datetime(df["date"])
            data = bt.feeds.PandasData(dataname=df, datetime="date", volume="volume")
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

    def prenext_open(self):
        if self.order:
            return

        # print(len(self.datas[0]))
        # print(len(self.datas[1]))
        # print(len(self.datas[2]))
        # print(len(self.datas[3]))
        # print(len(self.datas[4]))
        # self.log("proc dict:{}".format(self.proc), doprint=True)

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
                        data=self.datas[i],
                    )

        if max_proc > 0:
            # print('{} Send Buy, from data {}, open {}'.format(
            #     self.datas[max_index].datetime.date(),
            #     max_index,
            #     self.datas[max_index].open[0]
            # ))
            # print(type(self.datas[max_index].datetime.date()))
            # time_tmp = '9/2/2018'
            # if self.datas[max_index].datetime.date() == datetime.date.strftime(time_tmp, '%Y-%m-%d'):
            #     print("pause")
            # print("==== ", type(self.datas[max_index].datetime.date().strftime('%Y-%m-%d')), self.datas[max_index].datetime.date().strftime('%Y-%m-%d'))
            # if self.datas[max_index].datetime.date().strftime('%Y-%m-%d') == '2018-09-02':
            #     print('pause')
            size_ = self.broker.getcash() / self.datas[max_index].open[0]
            size_str = str(size_).split('.')[0] + '.' + str(size_).split('.')[1][:4]
            size_real = float(size_str)
            # diff_ = size_ * self.datas[max_index].open[0] - self.broker.getcash()
            # print("date = {}, price: {}, size: {}, cash: {}, diff: {}".format(self.datas[max_index].datetime.date(), self.datas[max_index].open[0], size_, self.broker.getcash(), diff_))
            self.order = self.buy(
                data=self.datas[max_index],
                size=size_real, #(self.broker.getcash() / self.datas[max_index].open[0]),
            )


        # pos_1 = self.getposition(data=self.datas[0])
        # pos_2 = self.getposition(data=self.datas[1])
        # print("position1: size = {}, price = {}, value = {}, cash = {}".format(pos_1.size, pos_1.price,
        #                                                                       pos_1.size * pos_1.price,
        #                                                                       self.broker.getcash()))
        # print("position2: size = {}, price = {}, value = {}, cash = {}".format(pos_2.size, pos_2.price,
        #                                                                       pos_2.size * pos_2.price,
        #                                                                       self.broker.getcash()))
        # print("position: size = {}, price = {}, value = {}, cash = {}".format(self.position.size, self.position.price, self.position.size * self.position.price, self.broker.getcash()))
        # print("position size: ", self.position.size)
        # print("position price: ", self.position.price)
            # dt = self.datas[max_index].datetime.date(-1)
            # self.order = self.buy(data=self.datas[max_index],
            #                       size=(self.broker.getcash() / self.datas[max_index].open[0]))


if __name__ == "__main__":
    ret, cerebro, ret_dict = PriceMomentumStrategyMultiData.run(
        data_path=["dataset/1d/LTC.csv", "dataset/1d/DOT.csv"],
        IS_ALL_IN=True,
        cash=10000000,
        params_dict={"strategy_params": {"time_period": 3, },
                     'analyzers': {
                         'sharp': bt.analyzers.SharpeRatio,
                         'annual_return': bt.analyzers.AnnualReturn,
                         'drawdown': bt.analyzers.DrawDown}}
    )

    print('Sharpe Ratio: ', ret[0].analyzers.sharp.get_analysis()["sharperatio"])
    print('annual return: ', ret[0].analyzers.annual_return.get_analysis())
    print('drawdown: ', ret[0].analyzers.drawdown.get_analysis()["max"]["drawdown"])
    print('-' * 200)
    print(ret_dict)
    # cerebro.plot(style='line')
