# -*- coding:utf-8 -*-
#
# Copyright (c) 2021 Hundsun.com, Inc. All Rights Reserved
#
"""
这个模块提供了backtrader流程的封装

@FileName  :  backtrader_pipeline.py
@Author    :  yujl
@Time      :  2021/4/19 18:53
"""

import os
import pathlib

import backtrader as bt
from backtrader import TimeFrame
import pandas as pd

class BTPipeline:
    def __init__(self, config_dict):
        """完成初始化工作

        实现初始化
        params:
            config_dict: 字典类型的参数，字段描述：
                suffix: 数据文件的后缀，默认为 '.csv'
                strategy: 策略类，列表类型，可以有多个，必须要有
                datetime: 数据时间列的位置。None：时间为index；-1：自动探测，大小写不敏感；>=0；位置索引；字符串：列的名称
                open：开盘价的位置。None：数据中没有这一列；-1：自动探测，大小写不敏感；>=0；位置索引；字符串：列的名称
                high：最高价的位置。None：数据中没有这一列；-1：自动探测，大小写不敏感；>=0；位置索引；字符串：列的名称
                low：最低价的位置。None：数据中没有这一列；-1：自动探测，大小写不敏感；>=0；位置索引；字符串：列的名称
                close：收盘价的位置。None：数据中没有这一列；-1：自动探测，大小写不敏感；>=0；位置索引；字符串：列的名称
                volume：交易量的位置。None：数据中没有这一列；-1：自动探测，大小写不敏感；>=0；位置索引；字符串：列的名称
                openinterest：未平仓量。None：数据中没有这一列；-1：自动探测，大小写不敏感；>=0；位置索引；字符串：列的名称
                time_frame：数据的频率。默认TimeFrame.Days（日数据）。其他支持频率：Ticks, MicroSeconds, Seconds, Minutes, Days, Weeks, Months, Years, NoTimeFrame
                from_date：数据起始日期。默认为None，以数据中最小的日期为起始日期
                to_data：数据截至日期。默认为None，以数据中最大的日期为截至日期
                cash：交易起始金额。默认为1000000
                commision：佣金。默认为0.001
                slip_style：滑点设置模式。默认为1。0为固定滑点，1为百分比滑点
                slip_value：滑点值。默认为0.001
                percent：每次购买的百分比。默认100，表示100%
                analyzer：回测评价指标，字典类型。
        """

        self.strategies = config_dict.get('strategy', None)
        if self.strategy == None:
            raise ValueError("The strategy is None")
        if not isinstance(self.strategy, list):
            raise ValueError("The strategy must be a list")

        self.suffix = config_dict.get('suffix', '.csv')

        self.datetime = config_dict.get('datetime', 'datetime')
        self.open = config_dict.get('open', 'open')
        self.high = config_dict.get('high', 'high')
        self.low = config_dict.get('low', 'low')
        self.close = config_dict.get('close', 'close')
        self.volume = config_dict.get('volume', 'volume')
        self.openinterest = config_dict.get('openinterest', None)
        self.time_frame = config_dict.get('time_frame', TimeFrame.Days)
        self.from_date = config_dict.get('frome_date', None)
        self.to_date = config_dict.get('to_date', None)

        self.cash = config_dict.get('cash', 1000000)
        self.commision = config_dict('commision', 0.001)
        self.slip_style = config_dict('slip_style', 1)      #
        self.slip_value = config_dict('slip_value', 0.001)
        self.buy_percent = config_dict('percent', 100)
        self.analyzers = config_dict('analyzer', {'sharp': bt.analyzers.SharpeRatio})

        self.cerebro = bt.Cerebro()

    def run(self, data_dir):
        """运行策略
        运行策略

        return:
            返回策略的结果
        """
        # 加载数据
        _dir = pathlib.Path(data_dir).expanduser()
        data_files = sorted(_dir.glob(f'*{self.suffix}'))
        for item in data_files:
            df = pd.read_csv(item)
            data = bt.feeds.PandasData(
                dataname=df,
                timeframe=self.time_frame,
                fromdate=self.from_date,
                todate=self.to_date,
                datetime=self.datetime,
                open=self.open,
                high=self.high,
                low=self.low,
                close=self.close,
                volume=self.volume,
                openinterest=self.openinterest,
            )
            self.cerebro.adddata(data)

        # 加载策略
        for strategy in self.strategies:
            self.cerebro.addstrategy(strategy)

        self.cerebro.broker.setcash(self.cash)
        self.cerebro.broker.setcommission(commission=self.commision)
        if self.slip_style == 1: #百分比滑点
            self.cerebro.broker.set_slippage_perc(self.slip_value)
        elif self.slip_style == 0: #固定滑点
            self.cerebro.broker.set_slippage_fixed(self.slip_value)
        else:
            raise ValueError("The slip style {} is not supported".format(self.slip_style))
        self.cerebro.addsizer(bt.sizers.PercentSizer, percents=self.buy_percent)

        # 加载回测指标
        for name, ana_class in self.analyzers:
            self.cerebro.addanalyzer(ana_class, _name=name)

        back_rets = self.cerebro.run()

        # self.cerebro.plot(style='candle')

        return back_rets


if __name__ == "__main__":
    pass