#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/4/6 16:57
# @Author  : Adolf
# @File    : by_turn_mul.py
# import numpy as np
import numpy as np
import pandas as pd
import ray

# import time
# import mplfinance as mlp
import matplotlib.pyplot as plt

pd.set_option("expand_frame_repr", False)
pd.set_option("display.max_rows", 1000)

trade_rate = 1.5 / 1000


@ray.remote
def turn_strategy(coin_list_, short_momentum_day_, long_momentum_day_):
    res_df = None
    for coin_name in coin_list_:
        # print(coin_name)
        df_ = pd.read_csv("dataset/1d/" + coin_name + ".csv")
        # print("coin name:", coin_name)
        # print("how long test:", len(df_))
        # print('=' * 20)
        df_[coin_name + '_pct'] = df_['close'].pct_change(periods=1)
        df_[coin_name + '_short_momentum'] = df_['close'].pct_change(periods=short_momentum_day_)
        df_[coin_name + '_long_momentum'] = df_['close'].pct_change(periods=long_momentum_day_)
        # print(df_)
        # exit()
        df_['time_stamp'] = pd.to_datetime(df_["time"], unit="ms")
        del df_['high'], df_['low'], df_['vol'], df_['time']
        df_ = df_[["time_stamp", "open", "close", coin_name + '_pct', coin_name + '_short_momentum',
                   coin_name + '_long_momentum']]
        df_.rename(columns={'open': coin_name + '_open', 'close': coin_name + '_close'}, inplace=True)
        # print(df)
        if res_df is None:
            res_df = df_
        else:
            res_df = pd.merge(left=res_df, right=df_, how='outer', on='time_stamp')
            # res_df = pd.concat([res_df, df_], axis=1, join='outer')

    # res_df = res_df.dropna(how="any")
    # res_df.reset_index(drop=True, inplace=True)

    # print(res_df)
    # exit()
    for index, row in res_df.iterrows():
        nb_coin_name = "empty"
        max_mom = 0
        for coin_name in coin_list:
            if not np.isnan(row[coin_name + '_long_momentum']) and row[coin_name + '_long_momentum'] > max_mom:
                max_mom = row[coin_name + '_long_momentum']
                nb_coin_name = coin_name
        # print(nb_coin_name)
        # print(max_mom)
        if max_mom > 0 and row[nb_coin_name + '_short_momentum'] > 0:
            res_df.loc[index, "style"] = nb_coin_name
        else:
            res_df.loc[index, "style"] = "empty"

    res_df['pos'] = res_df['style'].shift(1)
    res_df.dropna(subset=['pos'], inplace=True)

    del res_df["style"]
    res_df.loc[res_df['pos'] != res_df['pos'].shift(1), 'trade_time'] = res_df['time_stamp']

    for index, row in res_df.iterrows():
        # print(row["pos"])
        # print(row[row['pos'] + '_pct'])
        if row["pos"] == "empty":
            res_df.loc[index, "strategy_pct"] = 0.0
        elif isinstance(row["trade_time"], str):
            res_df.loc[index, "strategy_pct"] = row[row["pos"] + '_close'] / (
                    row[row["pos"] + '_open'] * (1 + trade_rate)) - 1
        else:
            res_df.loc[index, "strategy_pct"] = row[row["pos"] + '_pct']
        # break
    # # 扣除卖出手续费
    res_df.loc[(res_df['trade_time'].shift(-1).notnull()) & (res_df["pos"] != "empty"), 'strategy_pct'] = \
        (1 + res_df['strategy_pct']) * (1 - trade_rate) - 1
    res_df.reset_index(drop=True, inplace=True)
    for coin_name in coin_list:
        # res_df[coin_name + '_net'] = res_df[coin_name + '_close'] / res_df[coin_name + '_close'][0]
        res_df[coin_name + '_net'] = (1 + res_df[coin_name + '_pct']).cumprod()
    res_df['strategy_net'] = (1 + res_df['strategy_pct']).cumprod()

    # calculate maximum drawdown
    res_df['max2here'] = res_df['strategy_net'].expanding().max()
    res_df['dd2here'] = res_df['strategy_net'] / res_df['max2here'] - 1
    # 计算最大回撤，以及最大回撤结束时间
    end_date, max_draw_down = tuple(res_df.sort_values(by=['dd2here']).iloc[0][['time_stamp', 'dd2here']])
    # 计算最大回撤开始时间
    start_date = res_df[res_df['time_stamp'] <= end_date].sort_values(by='strategy_net', ascending=False).iloc[0][
        'time_stamp']
    # 将无关的变量删除
    res_df.drop(['max2here', 'dd2here'], axis=1, inplace=True)

    # return res_df, max_draw_down, start_date, end_date
    return res_df.tail(1)['strategy_net'].item(), max_draw_down, start_date, end_date


# coin_list = ["BTC", "ETH", "DOT", "ADA", "UNI", "EOS", "BNB", "XRP"]
coin_list = ["BTC", "ETH", "BNB", "DOT", "UNI", "CAKE"]
# coin_list = ["BTC", "ETH",]


# for i in range(3, 100):
#     strategy_net, max_draw_down, start_date, end_date = turn_strategy(coin_list, short_momentum_day_=i,
#                                                                       long_momentum_day_=i)
#     print(i)
#     print(strategy_net)
#     print(max_draw_down)
#     print('==========')


def ray_test(coin_list):
    ray.init()
    futures = [turn_strategy.remote(coin_list, short_momentum_day_=i, long_momentum_day_=i) for i in range(3, 101)]
    result = ray.get(futures)

    for i in range(len(result)):
        print(i + 3, result[i][:2])
    # print(result[i - 3][1])


ray_test(coin_list)
# momentum_day = 18
# for momentum_day in range(3, 31):
#     df = turn_strategy(coin_list, momentum_day_=momentum_day)
#     print(momentum_day, df.tail(1)["strategy_net"].item())
# res_list = list()
# for i in range(3, 101):
#     df, max_draw_down, start_date, end_date = turn_strategy(coin_list, short_momentum_day_=i, long_momentum_day_=i)
# print(len(df))
# print('time period:', i)
# print('strategy net:', df.tail(1)['strategy_net'].item())
# print('-' * 100)
# print(i, df.tail(1)['strategy_net'].item(),max_draw_down)
# print(max_draw_down)
# res_list.append(df.tail(1)['strategy_net'].item())
# print(df.columns)
# print('=' * 20)
# for columns_name in df.columns.tolist():
#     if "_net" not in columns_name:
#         continue
#     plt.plot(df['time_stamp'], df[columns_name], label=columns_name)
# break

# plt.plot(res_list)
# plt.show()
# plt.legend()
# plt.savefig("image/result.pdf", format="pdf")
# df.to_csv('result/20_btc_eth_ltc_bnb_turn.csv', index=False)
