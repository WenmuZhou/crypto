#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/6/17 9:33
# @Author   : Adolf
# @File     : ths_ls.py
# @Function  :

import pandas as pd
from strategy.personalise.loop_pos.strategy_srtucture.base_structure import TradeStructure
from strategy.personalise.loop_pos.utils.technical_indications import cal_ths_ls
from strategy.personalise.loop_pos.utils.signal_point import up_cross, down_cross

pd.set_option("expand_frame_repr", False)
pd.set_option("display.max_rows", 1000)


# 使用同花顺标注的多空点进行买卖操作
class TongHuaShunLongShort(TradeStructure):
    def cal_technical_index(self):
        self.base_technical_index(ma_parm=(10, 20,60), macd_parm=(12, 26, 9), kdj_parm=(9, 3))
        cal_ths_ls(self.data)
        up_cross(self.data, "var2", "var4", "long")
        down_cross(self.data, "var2", "var4", "short")

        self.data = self.data[-2000:]

    def get_buy_sell_signal(self, **kwargs):
        self.data.loc[
            self.data["long"]
            & ((self.data["close"] / self.data["MA60"]) > kwargs["MA_threshold"])
        ,"trade"] = "buy"
        self.data.loc[self.data["short"], "trade"] = "sell"
if __name__ == '__main__':
    ths_ls = TongHuaShunLongShort()
    # mawind.cal_technical_index()
    ths_ls.run_one_stock(data_path="/data3/stock_data/stock_data/real_data/bs/post_d/sz.002352.csv",
                         analyze_positions=True,
                         print_log=True,bs_signal_param={"MA_threshold": 0.1})

    # stock_list = []
    # with open("strategy/personalise/portfolio/stock_pooling.md", 'r') as f:
    #     for line in f.readlines():
    #         stock_id = line.strip().split(",")[1].replace(";", "")
    #         stock_list.append(stock_id)
    # ths_ls.run_all_market(data_dir="/data3/stock_data/stock_data/real_data/bs/post_d",
    #                       limit_list=stock_list,
    #                       save_result_path="result/ths_test.csv")
