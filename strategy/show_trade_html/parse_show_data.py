#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/5/23 12:32
# @Author   : Adolf
# @File     : parse_show_data.py
# @Function  :
import os
import pandas as pd
from strategy.personalise.chan_theory.chan_bi import ChanBi


def parse_data(stock_id="600570", level="day"):
    day_data_path = "/root/adolf/dataset/stock/d_pre/"
    if level == "day":
        if os.path.exists(os.path.join(day_data_path, "sz." + stock_id + ".csv")):
            df_path = os.path.join(day_data_path, "sz." + stock_id + ".csv")
        elif os.path.exists(os.path.join(day_data_path, "sh." + stock_id + ".csv")):
            df_path = os.path.join(day_data_path, "sh." + stock_id + ".csv")
        else:
            return {"error_msg": "不存在股票代码"}
    # print(df)
    show_json = ChanBi(df_path).run(make_plot=False, front_show=True)
    return show_json


if __name__ == '__main__':
    parse_data(stock_id="600570", level="day")
