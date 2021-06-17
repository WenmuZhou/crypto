#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/6/7 19:08
# @Author   : Adolf
# @File     : pool_data.py
# @Function  :
import os
# import shutil
import pandas as pd
import talib

pd.set_option("expand_frame_repr", False)
# data_dir = "/root/adolf/dataset/stock/d_post/"

# with open("strategy/personalise/portfolio/stock_pooling.md", 'r') as f:
#     for line in f.readlines():
#         stock_id = line.strip().split(",")[1].replace(";", "")
#         print(stock_id)
#         if stock_id[0] == "6":
#             stock_path = data_dir + "sh." + stock_id + ".csv"
#         else:
#             stock_path = data_dir + "sz." + stock_id + ".csv"
#
#         new_path = "dataset/stock/turn_stock_pooling/" + stock_id + ".csv"
#         shutil.copyfile(stock_path, new_path)
stock_dir = "dataset/stock/turn_stock_pooling/"
stock_handle_dir = "dataset/stock/stock_handle/"
stock_list = os.listdir(stock_dir)
for stock_csv in stock_list:
    print(stock_csv)
    df = pd.read_csv(os.path.join(stock_dir, stock_csv))

    del df["amount"], df["turn"], df["pctChg"], df["adjustflag"]
    df["ma5"] = df["close"].rolling(5).mean()
    df["ma10"] = df["close"].rolling(10).mean()

    df["ema12"] = talib.EMA(df["close"], timeperiod=12)
    df["ema26"] = talib.EMA(df["close"], timeperiod=26)

    df["MACD"] = df["ema12"] - df["ema26"]
    df["DEA"] = talib.EMA(df["MACD"], timeperiod=9)
    df.dropna(how="any",inplace=True)
    # print(df)
    df.to_csv(os.path.join(stock_handle_dir, stock_csv), index=False)
    # break
