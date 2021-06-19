#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/6/19 20:22
# @Author   : Adolf
# @File     : ma_cross.py
# @Function  :

import pandas as pd
from strategy.personalise.loop_pos.strategy_srtucture.base_structure import TradeStructure
from strategy.personalise.loop_pos.utils.signal_point import up_cross, down_cross

pd.set_option("expand_frame_repr", False)
pd.set_option("display.max_rows", 1000)


# 使用5日均线和10日均线交叉进行买卖
class SmaCross(TradeStructure):
    def cal_technical_index(self):
        self.base_technical_index(ma_parm=(5, 10, 20), macd_parm=(12, 26, 9), kdj_parm=(9, 3))

        up_cross(self.data, "MA5", "MA10", "long")
        down_cross(self.data, "MA5", "MA10", "short")

        self.data = self.data[-2000:]

if __name__ == '__main__':
    sc = SmaCross()
    # sc.cal_technical_index()
    sc.run_one_stock(data_path="/data3/stock_data/stock_data/real_data/bs/post_d/sh.600570.csv",
                     analyze_positions=True,
                     print_log=True)

    # stock_list = []
    # with open("strategy/personalise/portfolio/stock_pooling.md", 'r') as f:
    #     for line in f.readlines():
    #         stock_id = line.strip().split(",")[1].replace(";", "")
    #         stock_list.append(stock_id)
    # ths_ls.run_all_market(data_dir="/data3/stock_data/stock_data/real_data/bs/post_d",
    #                       limit_list=stock_list,
    #                       save_result_path="result/ths_test.csv")
