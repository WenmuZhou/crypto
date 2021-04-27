#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/4/27 19:35
# @Author   : Adolf
# @File     :
# price_rate_change_multi_analysis.py
# @Function  :
import backtrader as bt
from strategy.backtrader_base.price_rate_change_multidata import PriceMomentumStrategyMultiData

import ray


def one_strategy(data_path_, time_period_):
    ret, cerebro, ret_dict = PriceMomentumStrategyMultiData.run(
        data_path=data_path_,
        IS_ALL_IN=True,
        cash=10000000,
        params_dict={"strategy_params":
                         {"time_period": time_period_, },
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


data_path = ["dataset/1d/BTC.csv", "dataset/1d/ETH.csv"]
time_period = 5

one_strategy(data_path, time_period)
