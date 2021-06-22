#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/6/21 13:26
# @Author   : Adolf
# @File     : base_portfolio.py
# @Function  :
import os
# import ray
import pandas as pd
# import modin.pandas as pd
from tqdm import tqdm

# ray.init()
pd.set_option("expand_frame_repr", False)
pd.set_option("display.max_rows", 1000)


# print(df.head())


def init_position():
    return {"pos_asset": [],
            "buy_date": [],
            "buy_price": [],
            "sell_date": [],
            "sell_price": [],
            "holding_time": []}


def portfolio_day(_df):
    date_list = _df.date.unique().tolist()
    result = dict()
    result_list = []

    choose_num = 10

    for one_date in tqdm(date_list):
        df2 = _df[_df["date"] == one_date]

        df2 = df2[df2["value"] > 2e+10]
        df2 = df2[df2["Day20Gap"] < 0.15]
        df2 = df2[df2["close"] > df2["ma30"]]

        df2.sort_values(by="mom_20", inplace=True, ascending=False)
        df2.reset_index(drop=True, inplace=True)

        print(df2[:choose_num])
        exit()

    df_res = pd.DataFrame(result_list)
    # print(df_res)
    df_res.to_csv("dataset/stock/mom_turn.csv", index=False)


df = pd.read_csv("/root/adolf/dataset/stock/handle_stock/mom_pool_2016_06_08-2021_06_21.csv")
portfolio_day(_df=df)

df_ana = pd.read_csv("dataset/stock/mom_turn.csv")
df_ana["pct"] = df_ana["sell_price"] / df_ana["buy_price"] - 1
df_ana['strategy_net'] = (1 + df_ana['pct']).cumprod()
df_ana["pct_show"] = df_ana["pct"].apply(lambda x: format(x, '.2%'))

success_rate = len(df_ana[df_ana["pct"] > 0]) / len(df_ana)
odds = df_ana["pct"].mean()

print(df_ana)

print("策略成功率:{:.2f}%".format(success_rate * 100))
print("策略赔率:{:.2f}%".format(odds * 100))
