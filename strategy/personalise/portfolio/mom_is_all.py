#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/6/14 16:56
# @Author   : Adolf
# @File     : mom_is_all.py
# @Function  :
import math
import os
import talib

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
import ray

import datetime

pd.set_option("expand_frame_repr", False)
pd.set_option("display.max_rows", 1000)


# df = pd.read_csv("dataset/stock/stock_handle/600570.csv")
# df = df[-90:]
# df.reset_index(drop=True, inplace=True)
# del df["ma5"], df["ma10"], df["ema12"], df["ema26"], df["MACD"], df["DEA"]
#
# df["ln_close"] = df["close"].apply(math.log)
# df["index"] = list(range(len(df)))
# print(df)
# # sns.pairplot(df, x_vars=['index'], y_vars='close', size=7, aspect=0.8)
# # plt.scatter(df["index"], df["close"], alpha=0.6)
# # plt.show()
#
# x = np.array(df["index"])
# y = np.array(df["ln_close"])
# # print(np.array(x))
# slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
# mom = slope * r_value ** 2
# print(mom)

# slope:回归线的斜率
# intercept:截取回归线
# rvalue:相关系数
# pvalue:对于使用检验统计量的t-distribution的Wald检验，对于零假设为斜率为零的假设检验使用Two-sided p-value。
# stderr:估计梯度的标准误差。
# print(slope, intercept, r_value, p_value, std_err)


# plt.plot(x, y, 'o', label='original data')
# plt.plot(x, intercept + slope * x, 'r', label='fitted line')
# plt.legend()
# plt.show()

def cal_mom(df):
    df["ln_close"] = df["close"].apply(math.log)
    df["index"] = list(range(len(df)))
    x = np.array(df["index"])
    y = np.array(df["ln_close"])

    slope, _, r_value, _, _ = stats.linregress(x, y)
    mom = slope * r_value ** 2
    # print(mom)
    return mom


# mapping_dict = dict()
# with open("strategy/personalise/portfolio/stock_pooling.md", 'r') as f:
#     for line in f.readlines():
#         # print(line.strip())
#         map_list = line.strip().split(',')
#         # print(map_list)
#         mapping_dict[map_list[1].replace(';', '')] = map_list[0]

# df_path = "dataset/stock/stock_handle/"
# df_list = os.listdir(df_path)
# result = dict()
# for stock in df_list:
#     df = pd.read_csv(os.path.join(df_path, stock))
#     if len(df) < 100:
#         continue
#     # print(stock)
#     df = df[-60:]
#     mom = cal_mom(df)
#     # result[mapping_dict[stock.replace('.csv','')]] = mom
#     result[stock] = mom
#     # break
#
# result2 = sorted(result.items(), key=lambda d: d[1], reverse=True)
# result3 = [i[0] for i in result2]
# print(result3[:100])

df_path = "/root/adolf/dataset/stock/post_d"

df_list = os.listdir(df_path)


ray.init()


@ray.remote(num_cpus=20)
def cal_slope_mom(stock):
    df = pd.read_csv(os.path.join(df_path, stock))
    if len(df) < 100:
        return 0
    df["DayPct"] = df["close"] / df["open"] - 1
    df["Day5Pct"] = df["close"].pct_change(5)
    df["Day5Pct"] = df["Day5Pct"].shift(-5)

    df["Day20Pct"] = df["close"].pct_change(20)
    df["Day20Pct"] = df["Day5Pct"].shift(-20)

    df["ln_close"] = df["close"].apply(math.log)

    df["ma5"] = df["close"].rolling(5).mean()
    df["ma10"] = df["close"].rolling(10).mean()
    df["ma20"] = df["close"].rolling(20).mean()
    df["ma30"] = df["close"].rolling(30).mean()
    df["ma60"] = df["close"].rolling(60).mean()

    df["ema12"] = talib.EMA(df["close"], timeperiod=12)
    df["ema26"] = talib.EMA(df["close"], timeperiod=26)

    df["MACD"] = df["ema12"] - df["ema26"]
    df["DEA"] = talib.EMA(df["MACD"], timeperiod=9)

    for time_period in [20, 30, 60, 90]:
        x = np.array(range(time_period))
        # print(x)
        for index, row in df.iterrows():
            if index < time_period - 1:
                continue
            y = np.array(df.loc[index - time_period + 1:index, "ln_close"])

            slope, _, r_value, _, _ = stats.linregress(x, y)
            mom = slope * r_value ** 2
            df.loc[index, "slope_" + str(time_period)] = slope
            df.loc[index, "mom_" + str(time_period)] = mom

    df.dropna(inplace=True)
    del df["adjustflag"]
    # print(df.head(100))
    df.to_csv(os.path.join("/root/adolf/dataset/stock/handle_stock/mom_res", stock), index=False)
    return 0


# cal_slope_mom(stock="sh.600570.csv")


futures = [cal_slope_mom.remote(stock) for stock in df_list]
ray.get(futures)

def cal_one_day_mom(_df, _time_period=30):
    _df["ma60"] = _df["close"].rolling(60).mean()
    _df = _df[-_time_period:].copy()
    _df["ln_close"] = _df["close"].apply(math.log)
    _df["gap"] = _df["low"] / _df["high"].shift(1) - 1
    # _df["gap"] = _df["gap"]
    _df["gap"] = _df["gap"].apply(lambda x: max(x, 0))
    _df["long"] = _df["close"] > _df["ma60"]

    _df["value"] = _df["amount"] * 100 / _df["turn"]
    # _df = _df[_df["value"] > 1e+10]

    _df.fillna(0, inplace=True)
    x = np.array(range(_time_period))
    y = np.array(_df["ln_close"])

    slope, _, r_value, _, _ = stats.linregress(x, y)
    mom = slope * r_value ** 2

    gap_sum = sum(_df["gap"])
    return slope, mom, gap_sum, _df.tail(1)["long"].item(), _df.tail(1)["value"].item()


def one_day_choose():
    df_path_ = "/root/adolf/dataset/stock/real_data/bs/pre_d"
    df_list_ = os.listdir(df_path_)
    result_ = {
        "stock_name": [],
        "slope": [],
        "mom": [],
        "gap_sum": [],
        "long": [],
        "value": []
    }
    for stock in df_list_:
        df = pd.read_csv(os.path.join(df_path, stock))
        if len(df) < 100:
            continue
        slope, mom, gap_sum, long, value = cal_one_day_mom(df)
        result_["stock_name"].append(stock.replace(".csv", ""))
        result_["slope"].append(slope)
        result_["mom"].append(mom)
        result_["gap_sum"].append(gap_sum)
        result_["long"].append(long)
        result_["value"].append(value)

    result = pd.DataFrame(result_)
    result = result.sort_values(by="mom")
    result = result[result["long"]]
    result = result[result["gap_sum"] < 0.2]
    result = result[result["value"] > 1e+10]

    today = datetime.date.today()
    result.to_csv("/data3/stock_data/stock_data/real_data/bs/mom_choose/" + today.strftime("%y-%m-%d") + ".csv",
                  index=False)
    print(result)

# one_day_choose()

# df = pd.read_csv("/data3/stock_data/stock_data/real_data/bs/mom_choose/21-06-17.csv")
# print(df.tail(20))
