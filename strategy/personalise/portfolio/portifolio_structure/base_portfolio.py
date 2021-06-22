#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/6/21 13:26
# @Author   : Adolf
# @File     : base_portfolio.py
# @Function  :
import os
import ray
import pandas as pd
import modin.pandas as pd
from tqdm import tqdm

ray.init()
pd.set_option("expand_frame_repr", False)
pd.set_option("display.max_rows", 1000)


# print(df.head())


def init_position():
    return {"pos_asset": "",
            "buy_date": "",
            "buy_price": "",
            "sell_date": "",
            "sell_price": "",
            "holding_time": 0}


def analysis_day(_df):
    # _df.sort_values(by=["date", "code"], inplace=True)

    # print(_df)
    # exit()

    date_list = _df.date.unique().tolist()
    result = dict()
    result_list = []
    one_pos = init_position()

    choose_num = 0

    for one_date in tqdm(date_list):
        df2 = _df[_df["date"] == one_date]

        if one_pos["pos_asset"] != "" and one_pos["pos_asset"] not in df2.code.unique().tolist():
            continue

        if one_pos["pos_asset"] != "":
            pos_close_price = df2.loc[df2["code"] == one_pos["pos_asset"], "close"].item()

        df2 = df2[df2["value"] > 2e+10]
        df2 = df2[df2["Day20Gap"] < 0.15]
        df2 = df2[df2["close"] > df2["ma30"]]

        result["date"] = one_date

        df2['mom_all'] = df["mom_20"] + df["mom_30"] + df["mom_60"] + df["mom_90"]
        df2.sort_values(by="mom_all", inplace=True, ascending=False)
        df2.reset_index(drop=True, inplace=True)

        choose_list = df2.code.tolist()[:10]
        if one_pos["pos_asset"] not in choose_list and one_pos["pos_asset"] != "":
            one_pos["sell_price"] = pos_close_price
            one_pos["sell_date"] = one_date
            one_pos["holding_time"] += date_list.index(one_date)

            result_list.append(one_pos)
            one_pos = init_position()

        elif one_pos["pos_asset"] == "" and len(df2) > 0:
            one_pos["pos_asset"] = df2.loc[choose_num, "code"]
            one_pos["buy_price"] = df2.loc[choose_num, "close"]
            one_pos["buy_date"] = one_date
            one_pos["holding_time"] = - date_list.index(one_date)

    df_res = pd.DataFrame(result_list)
    # print(df_res)
    df_res.to_csv("dataset/stock/mom_turn.csv", index=False)


df = pd.read_csv("/root/adolf/dataset/stock/handle_stock/mom_pool_2016_06_08-2021_06_21.csv")
analysis_day(_df=df)

df_ana = pd.read_csv("dataset/stock/mom_turn.csv")
df_ana["pct"] = df_ana["sell_price"] / df_ana["buy_price"] - 1
df_ana['strategy_net'] = (1 + df_ana['pct']).cumprod()
df_ana["pct_show"] = df_ana["pct"].apply(lambda x: format(x, '.2%'))

success_rate = len(df_ana[df_ana["pct"] > 0]) / len(df_ana)
odds = df_ana["pct"].mean()

print(df_ana)

print("策略成功率:{:.2f}%".format(success_rate * 100))
print("策略赔率:{:.2f}%".format(odds * 100))