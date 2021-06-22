#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/6/15 16:08
# @Author   : Adolf
# @File     : analysis_mom.py
# @Function  :
import os.path
from tqdm import tqdm

import pandas as pd
# import ray
# import modin.pandas as pd

# ray.init()
pd.set_option("expand_frame_repr", False)
pd.set_option("display.max_rows", 1000)


def merge_mom_data():
    data_path = "/root/adolf/dataset/stock/handle_stock/mom_res/"
    data_list = os.listdir(data_path)
    df_list = []
    for data in tqdm(data_list):
        df = pd.read_csv(os.path.join(data_path, data))
        # df = df[df["date"] > "2016-06-07"]
        # original = len(df)
        df['code'] = data.replace(".csv", "")
        df["value"] = df["amount"] * 100 / df["turn"]
        # df = df[df["value"] > 1e+10]
        # if len(df) > 0 and len(df) / original > 0.5:
        # 上市超过半年
        if len(df) > 120:
            df_list.append(df)

    df_concat = pd.concat(df_list, ignore_index=True)
    df_concat.sort_values(by=["date", "code"], inplace=True)
    df_concat.to_csv("/root/adolf/dataset/stock/handle_stock/mom_pool.csv", index=False)


merge_mom_data()
# df = pd.read_csv("/root/adolf/dataset/stock/handle_stock/mom_pool.csv")
# df = df[df["date"] > "2016-06-07"]
# df.to_csv("/root/adolf/dataset/stock/handle_stock/mom_pool_2016_06_08-2021_06_21.csv", index=False)


def analysis_day():
    df = pd.read_csv("/root/adolf/dataset/stock/handle_stock/mom_pool_2016_06_08-2021_06_21.csv")
    df.sort_values(by=["date", "code"], inplace=True)

    date_list = df.date.unique()
    result = dict()
    result_list = []
    for one_date in tqdm(date_list):
        df2 = df[df["date"] == one_date]
        df2 = df2[df2["value"] > 1e+10]
        df2 = df2[df2["Day20Gap"] < 0.15]
        df2 = df2[df2["close"] > df2["ma30"]]

        result["date"] = one_date
        choose_num = 5
        df2.sort_values(by="mom_30", inplace=True)

        result["mom30_day_pct"] = df2.tail(choose_num)["DayPct"].mean()
        result["mom30_5day_pct"] = df2.tail(choose_num)["Day5Pct"].mean()
        result["mom30_20day_pct"] = df2.tail(choose_num)["Day20Pct"].mean()

        df2.sort_values(by="mom_20", inplace=True)

        result["mom20_day_pct"] = df2.tail(choose_num)["DayPct"].mean()
        result["mom20_5day_pct"] = df2.tail(choose_num)["Day5Pct"].mean()
        result["mom20_20day_pct"] = df2.tail(choose_num)["Day20Pct"].mean()

        df2.sort_values(by="mom_60", inplace=True)

        result["mom60_day_pct"] = df2.tail(choose_num)["DayPct"].mean()
        result["mom60_5day_pct"] = df2.tail(choose_num)["Day5Pct"].mean()
        result["mom60_20day_pct"] = df2.tail(choose_num)["Day20Pct"].mean()

        df2.sort_values(by="mom_90", inplace=True)

        result["mom90_day_pct"] = df2.tail(choose_num)["DayPct"].mean()
        result["mom90_5day_pct"] = df2.tail(choose_num)["Day5Pct"].mean()
        result["mom90_20day_pct"] = df2.tail(choose_num)["Day20Pct"].mean()

        result_list.append(result.copy())

    # print(result)
    df = pd.DataFrame(result_list)

    # print(df)
    # df.columns = ['date', 'pct_mean']
    df.to_csv("dataset/stock/mom_analysis.csv", index=False)


# analysis_day()
# #
# df = pd.read_csv("dataset/stock/mom_analysis.csv")
# # # print(df)
# # print(df.describe())
# # # df.sort_values()
# df_index = pd.read_csv("/data3/stock_data/stock_data/real_data/index/hu_shen_300.csv")
# df_index["ma60"] = df_index["close"].rolling(60).mean()
# #
# df_index = df_index[df_index["date"] > "2016-06-07"]
# df_index["niu"] = df_index["close"] > df_index["ma60"]
# df_index = df_index[["date", "niu"]]
# # #
# result = pd.merge(df, df_index, on=["date"])
# # # print(result)
# # #
# result2 = result[result["niu"]]
# # # print(result2)
# print(result2.describe())
