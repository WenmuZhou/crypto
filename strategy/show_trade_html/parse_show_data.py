#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/5/23 12:32
# @Author   : Adolf
# @File     : parse_show_data.py
# @Function  :
import os
from strategy.personalise.loop_pos.ma_wind import MaWind


def parse_data(stock_id="600570", level="day", start_time="", end_time=""):
    day_data_path = "/root/adolf/dataset/stock/d_pre/"
    if level == "day":
        if os.path.exists(os.path.join(day_data_path, "sz." + stock_id + ".csv")):
            df_path = os.path.join(day_data_path, "sz." + stock_id + ".csv")
        elif os.path.exists(os.path.join(day_data_path, "sh." + stock_id + ".csv")):
            df_path = os.path.join(day_data_path, "sh." + stock_id + ".csv")
        else:
            return {"error_msg": "不存在股票代码"}
    # print(df)
    show_json = MaWind(data_path=df_path)(show_buy_and_sell=True)
    print(show_json)
    return show_json


if __name__ == '__main__':
    parse_data(stock_id="600570", level="day")
