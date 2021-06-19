#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/6/19 22:04
# @Author   : Adolf
# @File     : param_analysis.py
# @Function  :
import os

import pandas as pd

from strategy.personalise.loop_pos.strategy_lib.macd import MACD

stock_list = []
with open("strategy/personalise/portfolio/stock_pooling.md", 'r') as f:
    for line in f.readlines():
        stock_id = line.strip().split(",")[1].replace(";", "")
        stock_list.append(stock_id)

macd = MACD()
data_dir = "/data3/stock_data/stock_data/real_data/bs/post_d"
data_list = os.listdir(data_dir)

parm_list = [-0.01, -0.1]
result_param_analysis = {
    "stock_id": [],
    "price": [],
    "stock_pct": [],
    "asset_pct_annual_return": [],
    "asset_wave": [],
    # "best_threshold": [],
    # "best_strategy_pct": [],
    # "best_strategy_annual_return": []
}

for parm in parm_list:
    result_param_analysis["macd_" + str(parm)] = []

for stock in data_list:
    if stock.split(".")[1] not in stock_list:
        continue
    for parm in parm_list:
        result_eval = macd.run_one_stock(data_path=os.path.join(data_dir, stock),
                                         bs_signal_param={"macd_threshold": parm})
        result_param_analysis["macd_" + str(parm)].append(
            str(result_eval["trade_nums"]) + "," + str(result_eval["odds"]) + "," + str(result_eval["strategy_pct"]))
    result_param_analysis["stock_id"].append(stock.replace(".csv",""))
    result_param_analysis["price"].append(macd.data.close.tail(1).item())
    result_param_analysis["stock_pct"].append(result_eval["asset_pct"])
    result_param_analysis["asset_pct_annual_return"].append(result_eval["asset_pct_annual_return"])
    result_param_analysis["asset_wave"].append(macd.data.ATR.tail(1).item())


result = pd.DataFrame(result_param_analysis)
result.to_csv("result/macd_threshold.csv", index=False)
