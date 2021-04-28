#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/4/21 9:26
# @Author   : Adolf
# @File     : two_sma.py
# @Function  :

import backtrader as bt
import pandas as pd
from backtrader.indicators import MovingAverageSimple

from strategy.backtrader_base.background_logic import BasisStrategy


class TwoSmaStrategy(BasisStrategy):
    """双均线策略
    《151 Trading Strategies》P50
    需要计算两类均值：短周期均值和长周期均值。当短周期均值穿过长周期均值买入，否则卖出
    Attributes:
        sma5: 短周期均值
        sma10: 长周期均值
    """
    params = (('short_period', 5), ('long_period', 10))

    # def __init__(self):
    #     super(TwoSmaStrategy, self).__init__()

    @staticmethod
    def data_process(data_path):
        df = pd.read_csv(data_path)
        df["date"] = pd.to_datetime(df["date"])
        data = bt.feeds.PandasData(dataname=df, datetime="date", volume="volume")
        return data

    def cal_technical_index(self):
        self.sma_short = bt.indicators.MovingAverageSimple(self.datas[0], period=self.params.short_period)
        self.sma_long = bt.indicators.MovingAverageSimple(self.datas[0], period=self.params.long_period)

    def next(self):
        # self.log('Open,%.2f' % self.datas[0].open[0])
        # self.log('Close, %.2f' % self.data_close[0])
        # self.log(self.position.size, doprint=True)

        if self.order:
            return

        if not self.position:
            if self.sma_short[0] > self.sma_long[0] and self.sma_short[-1] > self.sma_long[-1]:
                # buy_size = int(self.broker.getcash() / self.data_close[0]) - 1
                # now_cash = self.broker.getcash()
                # now_price = self.data_close[0]

                # self.log("应该所剩余额:{}".format(now_cash - now_price * buy_size), doprint=True)
                # self.log("目前是买点,目前拥有的现金:{},目前的收盘价是:{},买入份额:{},手续费:{}".format(now_cash, now_price,
                #                                                              buy_size,
                #                                                              self.buy_comm),
                #          doprint=True)
                # self.log("购买时的价格：{}".format(self.datas[0].open[1]))
                self.order = self.buy(size=(self.broker.getcash() / self.datas[0].open[0]))
                # print(self.order)
        else:
            if self.sma_short[0] < self.sma_long[0]:
                # self.log("卖出前:{}".format(self.position.size))
                self.order = self.sell(size=self.position.size)


if __name__ == '__main__':
    TwoSmaStrategy.run(data_path="dataset/1d/BTC.csv", cash=100000000, commission=0, IS_ALL_IN=True)
