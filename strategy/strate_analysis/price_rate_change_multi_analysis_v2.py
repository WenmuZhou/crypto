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
# import ray
from ray import tune


class StrategyParamOptim:
    def __init__(self, data_dir_path):
        self.data_dir_path = data_dir_path
        self.data_list = os.listdir(data_dir_path)

    @staticmethod
    def one_strategy(data_path_, time_period_):
        ret, cerebro, ret_dict = PriceMomentumStrategyMultiData.run(data_path=data_path_, cash=10000000, IS_ALL_IN=True,
                                                                    params_dict={"strategy_params": {
                                                                        "time_period": time_period_, },
                                                                                 'analyzers': {
                                                                                     'sharp': bt.analyzers.SharpeRatio,
                                                                                     'annual_return': bt.analyzers.AnnualReturn,
                                                                                     'drawdown': bt.analyzers.DrawDown}})
        ret_dict["drawdown"] = ret[0].analyzers.drawdown.get_analysis()["max"]["drawdown"]
        return ret_dict

    def get_combination_list(self):
        combinations_list = list()
        for i in range(2, len(self.data_list) + 1):
            combinations_list.extend(list(combinations(self.data_list, i)))

        return combinations_list

    def one_config_function(self, one_combination, time_period):
        # combinations_list = self.get_combination_list()
        # combinations_list_ = config["combinations_list"]
        # time_period_list_ = config["time_period_list"]

        # for one_combination in combinations_list_[:20]:
        data_path = [os.path.join(self.data_dir_path, name) for name in one_combination]
        # for time_period in time_period_list_:
        result = self.one_strategy(data_path, time_period)
        coin_yield = []
        coin_yield_max = max(result.values())
        for key, value in result.items():
            if "coin_yield" in key:
                coin_yield.append(str(round(value, 3)))
        tmp_list = [','.join([i.replace(".csv", "") for i in one_combination]),
                    time_period, ",".join(coin_yield),
                    round(result["strategy_yield"], 3),
                    round(result["drawdown"], 3),
                    result["strategy_yield"] > coin_yield_max]
        # print(tmp_list)
        # print('---------------')

        return tmp_list
        # res_list.append(tmp_list)
        #
        # df_ = pd.DataFrame(res_list,
        #                    columns=["coin", "time_period", "coin_yield", "strategy_yield", "drawdown", "is_win"])
        # return df_

    def training_function(self, config):
        combinations_list_ = config["combinations_list"]
        time_period_ = config["time_period"]
        for step in range(100000):
            intermediate_score = self.one_config_function(combinations_list_, time_period_)[3]
            tune.report(mean_loss=intermediate_score)

    def __call__(self):
        combinations_list = self.get_combination_list()
        analysis = tune.run(
            strategy_param_optim.training_function,
            config={
                "combinations_list": tune.choice(combinations_list),
                "time_period": tune.choice(list(range(3, 250)))
            })

        print("Best config: ", analysis.get_best_config(metric="mean_loss", mode="max"))

        # Get a dataframe for analyzing trial results.
        df = analysis.results_df

        return df


if __name__ == '__main__':
    strategy_param_optim = StrategyParamOptim(data_dir_path="/root/adolf/crypto/dataset/1d")

    df = strategy_param_optim()
    df.to_csv("/root/adolf/crypto/result/all_test_v2.csv")
