#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/4/28 16:11
# @Author   : Adolf
# @File     : two_ma_analysis.py
# @Function  :
import os
import pandas as pd
import backtrader as bt
from strategy.backtrader_base.two_sma import TwoSmaStrategy

data_dir = "/root/adolf/dataset/d"
data_list = os.listdir(data_dir)

# print(data_list)

for data_name in data_list:
    # df = pd.read_csv(os.path.join(data_dir, data_name))
    data_path = os.path.join(data_dir, data_name)
    # print(df)
    ret, cerebro, ret_dict = TwoSmaStrategy.run(
        data_path=data_path,
        IS_ALL_IN=True,
        params_dict={"strategy_params":
                         {"short_period": 5,
                          "long_period": 10},
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

    break
