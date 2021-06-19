#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/5/23 12:32
# @Author   : Adolf
# @File     : parse_show_data.py
# @Function  :
import os
from strategy.personalise.loop_pos.strategy_lib.ma_wind import MaWind


def parse_data(stock_id="600570", time_period="day", start_time="", end_time=""):
    day_data_path = "/root/adolf/dataset/stock/d_pre/"
    min_data_base_path = "/root/adolf/dataset/stock/jy_data/"
    if time_period == "day":
        if os.path.exists(os.path.join(day_data_path, "sz." + stock_id + ".csv")):
            df_path = os.path.join(day_data_path, "sz." + stock_id + ".csv")
        elif os.path.exists(os.path.join(day_data_path, "sh." + stock_id + ".csv")):
            df_path = os.path.join(day_data_path, "sh." + stock_id + ".csv")
        else:
            return {"error_msg": "不存在股票代码"}
    elif "min" in time_period:
        min_data_path = os.path.join(min_data_base_path,time_period)
        if os.path.exists(os.path.join(min_data_path, stock_id + ".SZ.csv")):
            df_path = os.path.join(min_data_path, stock_id + ".SZ.csv")
        elif os.path.exists(os.path.join(min_data_path, stock_id + ".SH.csv")):
            df_path = os.path.join(min_data_path, stock_id + ".SH.csv")
        else:
            return {"error_msg": "不存在股票代码"}
    # print(df)
    else:
        return {"error_msg": "不存在的时间周期"}

    # print(df_path)
    show_json = MaWind(data_path=df_path)(show_buy_and_sell=True)
    # print(show_json)
    return show_json


if __name__ == '__main__':
    parse_data(stock_id="600570", time_period="30min")
