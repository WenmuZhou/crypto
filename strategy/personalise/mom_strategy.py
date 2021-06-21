#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/5/18 14:14
# @Author   : Adolf
# @File     : mom_strategy.py
# @Function  :
import os
import pandas as pd
from functools import reduce
import matplotlib.pyplot as plt

pd.set_option("expand_frame_repr", False)
pd.set_option("display.max_rows", 2000)


class MomStrategy:
    def __init__(self, _coin_list, _time_period):
        self.coin_list = _coin_list
        self.time_period = _time_period
        self.trade_rate = 1 / 1000
        self.df_merge = self.merge_all_df()
        self.my_position = self.init_my_position()
        print("本次共用到的K线数量是:", len(self.df_merge))
        # self.momentum_day = 5

    @staticmethod
    def init_my_position():
        return {
            "date": "",
            "pre_close": 1,
            "pre_style": "USDT",
            "style_close": 1,
            "pos_style": "USDT",
            "my_value": 1,
            "is_turn": False}

    def merge_all_df(self):
        data_frames = []
        for coin_name in self.coin_list:
            # df_dir = "/data3/stock_data/stock_data/real_data/index"
            df_dir = "/data3/stock_data/stock_data/real_data/index"

            # df_dir = "dataset/" + self.time_period + "/" + coin_name + "_USDT_" + self.time_period
            # df_list = os.listdir(df_dir)
            # exit()
            df = pd.read_csv(os.path.join(df_dir, coin_name+".csv"))
            # del df['time'], df['high'], df['low'], df['vol']
            df = df[['date', 'open', 'close']]
            df[coin_name + '_pct'] = df['close'].pct_change(periods=1)
            # df[coin_name + '_momentum'] = df['close'].pct_change(periods=_momentum_day)
            df.rename(columns={'open': coin_name + '_open',
                               'close': coin_name + '_close'},
                      inplace=True)
            # print(df)
            data_frames.append(df)

        df_merged = reduce(lambda left, right: pd.merge(left, right, on=['date'],
                                                        how='outer'), data_frames)
        df_merged.sort_values(by=['date'], inplace=True)
        df_merged["USDT_close"] = 1
        df_merged["USDT_pct"] = 0
        df_merged.dropna(inplace=True)
        return df_merged

    def trade_process(self, momentum_day):
        for coin_name in coin_list:
            self.df_merge[coin_name + '_momentum'] = self.df_merge[coin_name + '_close'].pct_change(
                periods=momentum_day)

        self.my_position = self.init_my_position()
        my_position_list = []
        for index, row in self.df_merge.iterrows():
            self.my_position["date"] = row["date"]
            max_momentum = 0
            coin_style = "USDT"
            for coin_name in self.coin_list:
                if not pd.isnull(row[coin_name + '_momentum']):
                    # print(coin_name)
                    if row[coin_name + '_momentum'] > max_momentum:
                        max_momentum = row[coin_name + '_momentum']
                        coin_style = coin_name
            self.my_position["pre_close"] = self.my_position["style_close"]
            self.my_position["pre_style"] = self.my_position["pos_style"]

            # my_position["style_close"] = row[my_position["pos_style"] + "_close"]
            # my_position["my_value"] *= (1 + my_position["style_close"] / my_position["pre_close"])
            self.my_position["is_turn"] = False

            if max_momentum > 0 and self.my_position["pos_style"] != coin_style:
                self.my_position["my_value"] *= (1 - self.trade_rate)
                self.my_position["pos_style"] = coin_style
                self.my_position["is_turn"] = True

            self.my_position["style_close"] = row[self.my_position["pos_style"] + "_close"]
            if not self.my_position["is_turn"]:
                self.my_position["my_value"] *= (1 + row[self.my_position["pos_style"] + "_pct"])
            else:
                self.my_position["my_value"] *= (1 + row[self.my_position["pre_style"] + "_pct"])

            # print(self.my_position)
            # my_position_list.append(self.my_position.copy())

    def run(self):
        for mom_day in range(10,30):
            self.trade_process(momentum_day=mom_day)
            print("momentum long", mom_day)
            print(self.my_position["my_value"])
            print('=' * 20)
        # my_position_df = pd.DataFrame(my_position_list)
        # print(my_position_df)
        # my_position_df = my_position_df[-300:]

        # my_position_df['max2here'] = my_position_df['my_value'].expanding().max()
        # my_position_df['dd2here'] = my_position_df['my_value'] / my_position_df['max2here'] - 1
        # 计算最大回撤，以及最大回撤结束时间
        # end_date, max_draw_down = tuple(my_position_df.sort_values(by=['dd2here']).iloc[0][['date', 'dd2here']])
        # 计算最大回撤开始时间
        # start_date = \
        #     my_position_df[my_position_df['date'] <= end_date].sort_values(by='my_value', ascending=False).iloc[0][
        #         'date']
        # 将无关的变量删除
        # my_position_df.drop(['max2here', 'dd2here'], axis=1, inplace=True)

        # my_position_df.to_csv("result/turn_30min.csv")
        # plt.plot(my_position_df['date'], my_position_df['my_value'], label='strategy')
        # plt.show()


if __name__ == '__main__':
    coin_list = ["hu_shen_300","zhong_zheng_500"]
    momstrage = MomStrategy(_coin_list=coin_list, _time_period="1m")
    momstrage.run()
    # print(momstrage.df_merge)
