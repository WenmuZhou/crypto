#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/4/28 14:45
# @Author   : Adolf
# @File     : price_rate_change_multi_analysis_v2.py
# @Function  :
import os

import backtrader as bt
import pandas as pd

from strategy.backtrader_base.price_rate_change_multidata import PriceMomentumStrategyMultiData
from itertools import combinations
import ray

ray.init()


@ray.remote(num_cpus=20)
class StrategyParamOptim:
    def __init__(self, data_dir_path, time_period):
        self.data_dir_path = data_dir_path
        self.data_list = os.listdir(data_dir_path)
        self.time_period = time_period

    @staticmethod
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

    def get_combination_list(self):
        combinations_list = list()
        for i in range(2, len(self.data_list) + 1):
            combinations_list.extend(list(combinations(self.data_list, i)))

        return combinations_list

    def one_config_function(self):
        combinations_list_ = self.get_combination_list()

        result_list = []
        for one_combination in combinations_list_:
            # print("one_combination:", one_combination)
            # print("time_period", time_period)
            data_path = [os.path.join(self.data_dir_path, name) for name in one_combination]
            # for time_period in time_period_list_:
            result = self.one_strategy(data_path, self.time_period)
            coin_yield = []
            coin_yield_max = 0
            for key, value in result.items():
                if "coin_yield" in key:
                    if value > coin_yield_max:
                        coin_yield_max = round(value, 3)
                    coin_yield.append(str(round(value, 3)))
            tmp_list = [','.join([i.replace(".csv", "") for i in one_combination]),
                        self.time_period, ",".join(coin_yield),
                        round(result["strategy_yield"], 3),
                        round(result["drawdown"], 3),
                        result["strategy_yield"] > coin_yield_max]
            print(tmp_list)
            # print('---------------')
            result_list.append(tmp_list)
        return result_list
        # res_list.append(tmp_list)
        #
        # df_ = pd.DataFrame(res_list,
        #                    columns=["coin", "time_period", "coin_yield", "strategy_yield", "drawdown", "is_win"])
        # return df_


if __name__ == '__main__':
    # strategy_param_optim = StrategyParamOptim(data_dir_path="dataset/1d")
    counters = [StrategyParamOptim.remote(data_dir_path="/root/adolf/crypto/dataset/1d", time_period=i) for i in
                range(3, 181)]
    futures = [c.one_config_function.remote() for c in counters]
    res_list = []
    # print(ray.get(futures))
    #     res_list.extend(ray.get(futures))
    #
    # # print(res_list)
    for one_res in ray.get(futures):
        res_list.extend(one_res)
    df = pd.DataFrame(res_list,
                      columns=["coin", "time_period", "coin_yield", "strategy_yield", "drawdown", "is_win"])

    # print(df)
    df.to_csv("/root/adolf/crypto/result/prc_mul_day.csv")
