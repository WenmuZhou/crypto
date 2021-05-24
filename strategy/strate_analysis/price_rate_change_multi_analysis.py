#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/4/27 19:35
# @Author   : Adolf
# @File     :
# price_rate_change_multi_analysis.py
# @Function  :
import os

import backtrader as bt
import pandas as pd

from strategy.backtrader_base.price_rate_change_multidata import PriceMomentumStrategyMultiData

from itertools import combinations

pd.set_option('expand_frame_repr', False)


# @ray.remote
def one_strategy(data_path_, time_period_):
    ret, cerebro, ret_dict = PriceMomentumStrategyMultiData.run(data_path=data_path_, cash=10000000, IS_ALL_IN=True,
                                                                params_dict={"strategy_params":
                                                                                 {"time_period": time_period_, },
                                                                             'analyzers': {
                                                                                 'sharp': bt.analyzers.SharpeRatio,
                                                                                 'annual_return': bt.analyzers.AnnualReturn,
                                                                                 'drawdown': bt.analyzers.DrawDown}})

    # print('Sharpe Ratio: ', ret[0].analyzers.sharp.get_analysis()["sharperatio"])
    # print('annual return: ', ret[0].analyzers.annual_return.get_analysis())
    # print('drawdown: ', ret[0].analyzers.drawdown.get_analysis()["max"]["drawdown"])
    # print('-' * 200)
    # print(ret_dict)
    ret_dict["drawdown"] = ret[0].analyzers.drawdown.get_analysis()["max"]["drawdown"]
    return ret_dict


data_dir_path = "dataset/1d/"
data_list = os.listdir(data_dir_path)
# print(data_list)
combinations_list = []
for i in range(2, len(data_list) + 1):
    combinations_list.append(list(combinations(data_list, i)))
# print(combinations_list)
res_list = []
for combinations_one_list in combinations_list[:10]:
    for one in combinations_one_list:
        # print(one)
        data_path = [os.path.join(data_dir_path, name) for name in one]
        # print(data_path)
        for time_period in range(3, 101):
            result = one_strategy(data_path, time_period)
            # print(result)
            coin_yield = []
            # print(result)
            # coin_yield_max = max(result.values())
            # print(coin_yield_max)
            coin_yield_max = 0
            for key, value in result.items():
                if "coin_yield" in key:
                    if value > coin_yield_max:
                        coin_yield_max = round(value, 3)
                    coin_yield.append(str(round(value, 3)))
            # print(coin_yield_max)
            tmp_list = [','.join([i.replace(".csv", "") for i in one]),
                        time_period, ",".join(coin_yield),
                        round(result["strategy_yield"], 3),
                        round(result["drawdown"], 3),
                        result["strategy_yield"] > coin_yield_max]
            # print(tmp_list)
            res_list.append(tmp_list)
        # break
    # break
# print(res_list)
df = pd.DataFrame(res_list, columns=["coin", "time_period", "coin_yield", "strategy_yield", "drawdown", "is_win"])
print(df)
df.to_csv("result/all_PRC_mul.csv", index=False)
# print(res_df))
# data_path = ["dataset/1d/BTC.csv", "dataset/1d/ETH.csv"]
# time_period = 5
#
# result = one_strategy(data_path, time_period)
# print(result)
