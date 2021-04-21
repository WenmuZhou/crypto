# -*- coding:utf-8 -*-
#
# Copyright (c) 2021 Hundsun.com, Inc. All Rights Reserved
#
"""
这个模块提供了

@FileName  :  run_strategy.py
@Author    :  yujl
@Time      :  2021/4/21 10:45
"""

from strategy.backtrader_base.ketler_v2 import KetlerStrategy
from strategy.backtrader_base.ssa import SSAStrategy
from strategy.backtrader_base.turtle import TurtleStrategy
from strategy.backtrader_base.price_rate_change import PriceMomentumStrategy
from strategy.backtrader_base.pivot_point import PivotStrategy

if __name__ == "__main__":
    # KetlerStrategy.run(data_path=r"F:\\stock_data\hs300_d\\sz.000001.csv")
    # SSAStrategy.run(data_path=r"F:\\stock_data\hs300_d\\sz.000001.csv")
    TurtleStrategy.run(data_path=r"F:\\stock_data\hs300_d\\sz.000001.csv")
    # PriceMomentumStrategy.run(data_path=r"F:\\stock_data\hs300_d\\sz.000001.csv")
    # PivotStrategy.run(data_path=r"F:\\stock_data\hs300_d\\sz.000001.csv")
