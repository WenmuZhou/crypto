#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/6/15 16:08
# @Author   : Adolf
# @File     : analysis_mom.py
# @Function  :
import os.path

import pandas as pd

pd.set_option("expand_frame_repr", False)
pd.set_option("display.max_rows", 1000)


def merge_mom_data():
    data_path = "/data3/stock_data/stock_data/real_data/bs/post_d/"
    data_list = os.listdir(data_path)
    df_list = []
    for data in data_list:
        df = pd.read_csv(os.path.join(data_path, data))
        df = df[df["date"] > "2016-06-07"]
        # original = len(df)
        df['code'] = data.replace(".csv", "")
        df["value"] = df["amount"] * 100 / df["turn"]
        # df = df[df["value"] > 1e+10]
        # if len(df) > 0 and len(df) / original > 0.5:
        # 上市超过半年
        if len(df) > 120:
            df_list.append(df)

    df_concat = pd.concat(df_list, ignore_index=True)
    df_concat.sort_values(by=["date", "code"])
    df_concat.to_csv("dataset/stock/mom_pool.csv", index=False)


# merge_mom_data()


def analysis_day():
    df = pd.read_csv("dataset/stock/mom_pool.csv")
    date_list = df.date.unique()
    result = dict()
    for one_date in date_list:
        df2 = df[df["date"] == one_date]
        df2 = df2.sort_values(by="mom_30")

        # result[one_date] = df2.tail(10)["Day5Pct"].mean()
        print(df2)
        exit()
        # result[one_date] = df2.tail(10)["DayPct"].mean()
    # df = pd.DataFrame(result, index=['pct']).T
    # df.columns = ['date', 'pct_mean']
    # df.to_csv("dataset/stock/mom_analysis.csv")


analysis_day()

# df = pd.read_csv("dataset/stock/mom_analysis.csv")
# # print(df)
# print(df.describe())
# # df.sort_values()
# df_index = pd.read_csv("/data3/stock_data/stock_data/real_data/index/hu_shen_300.csv")
# df_index["ma60"] = df_index["close"].rolling(60).mean()
#
# df_index = df_index[df_index["date"] > "2016-06-07"]
# df_index["niu"] = df_index["close"] > df_index["ma60"]
# df_index = df_index[["date", "niu"]]
#
# result = pd.merge(df, df_index, on=["date"])
# # print(result)
#
# result2 = result[result["niu"]]
# # print(result2)
# print(result2.describe())
