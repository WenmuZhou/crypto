#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/5/2 17:01
# @Author   : Adolf
# @File     : price_rate_change_multi_analysis_v4.py
# @Function  :
import os

import backtrader as bt
import pandas as pd

from strategy.backtrader_base.price_rate_change_multidata import PriceMomentumStrategyMultiData
from itertools import combinations

from sko.GA import GA

pd.set_option('expand_frame_repr', False)


def one_strategy(data_path_, time_period_):
    ret, cerebro, ret_dict = PriceMomentumStrategyMultiData.run(
        data_path=data_path_,
        IS_ALL_IN=True,
        cash=10000000,
        params_dict={"strategy_params": {"time_period": time_period_, },
                     'analyzers': {
                         'sharp': bt.analyzers.SharpeRatio,
                         'annual_return': bt.analyzers.AnnualReturn,
                         'drawdown': bt.analyzers.DrawDown}}
    )
    ret_dict["drawdown"] = ret[0].analyzers.drawdown.get_analysis()["max"]["drawdown"]
    return ret_dict


data_dir_path = "dataset/1d/"
data_list = os.listdir(data_dir_path)
combinations_list = []
for i in range(2, len(data_list) + 1):
    combinations_list.extend(list(combinations(data_list, i)))


# res_list = []

# print(len(combinations_list))


def task(p):
    combination_index, time_period = p
    # print(combinations_list[combination_index])
    data_path = [os.path.join(data_dir_path, name) for name in combinations_list[int(combination_index)]]
    # print(data_path)
    result = one_strategy(data_path, int(time_period))
    return -result["strategy_yield"]


p = (0, 3)
# print(task(p))
ga = GA(func=task, n_dim=2, size_pop=100, max_iter=10000, lb=[0, 3], ub=[len(combinations_list) - 1, 250], prob_mut=0.1,
        precision=1)
best_x, best_y = ga.run()
print('best_x:', best_x, '\n', 'best_y:', best_y)
# for one_combination in combinations_list:
#     print(one_combination)
#     data_path = [os.path.join(data_dir_path, name) for name in one_combination]
#     time_period = 3
#     result = one_strategy(data_path, time_period)
#     coin_yield = []
#     coin_yield_max = max(result.values())
#     for key, value in result.items():
#         if "coin_yield" in key:
#             coin_yield.append(str(round(value, 3)))
#     tmp_list = [','.join([i.replace(".csv", "") for i in one_combination]),
#                 time_period, ",".join(coin_yield),
#                 round(result["strategy_yield"], 3),
#                 round(result["drawdown"], 3),
#                 result["strategy_yield"] > coin_yield_max]
#     res_list.append(tmp_list)
# df = pd.DataFrame(res_list, columns=["coin", "time_period", "coin_yield", "strategy_yield", "drawdown", "is_win"])
# print(df)
# df.to_csv("result/all_test_v4.csv", index=False)
