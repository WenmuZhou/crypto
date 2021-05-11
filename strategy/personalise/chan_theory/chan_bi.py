#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/5/10 10:06
# @Author   : Adolf
# @File     : chan_bi.py
# @Function  :
import pandas as pd
import matplotlib.pyplot as plt

pd.set_option("expand_frame_repr", False)
pd.set_option("display.max_rows", 1000)


class ChanBi:
    def __init__(self, data_path):
        df = pd.read_csv(data_path)
        self.df = df[-1000:]
        self.df.reset_index(drop=True, inplace=True)
        self.merge_data = []
        self.butch_list = []
        self.femme_list = []
        self.markers_on = []

    def k_data_handle(self):
        one_k_info = {"high_date": "",
                      "low_date": "",
                      "high_value": "",
                      "low_value": "", }
        for index, row in self.df.iterrows():
            if len(self.merge_data) == 0:
                one_k_info["high_date"] = row["date"]
                one_k_info["low_date"] = row["date"]
                one_k_info["high_value"] = row["high"]
                one_k_info["low_value"] = row["low"]
                self.merge_data.append(one_k_info.copy())
            else:
                pre_dict = self.merge_data[-1]
                pre_high = pre_dict["high_value"]
                pre_low = pre_dict["low_value"]
                pre_high_date = pre_dict["high_date"]
                pre_low_date = pre_dict["low_date"]
                if (row["high"] >= pre_high and row["low"] <= pre_low) or (
                        row["high"] <= pre_high and row["low"] >= pre_low):
                    if len(self.merge_data) > 1:
                        pre_plus_dict = self.merge_data[-2]
                        pre_plus_high = pre_plus_dict["high_value"]
                    else:
                        pre_plus_high = 0
                    self.merge_data.pop()
                    if pre_high > pre_plus_high:
                        now_high = max(row["high"], pre_high)
                        now_low = max(row["low"], pre_low)
                    else:
                        now_high = min(row["high"], pre_high)
                        now_low = min(row["low"], pre_low)

                    if now_high == row["high"]:
                        now_high_date = row["date"]
                    else:
                        now_high_date = pre_high_date

                    if now_low == row["low"]:
                        now_low_date = row["date"]
                    else:
                        now_low_date = pre_low_date
                else:
                    now_high = row["high"]
                    now_low = row["low"]
                    now_high_date = row["date"]
                    now_low_date = row["date"]

                one_k_info["high_date"] = now_high_date
                one_k_info["low_date"] = now_low_date
                one_k_info["high_value"] = now_high
                one_k_info["low_value"] = now_low
                self.merge_data.append(one_k_info.copy())

    def get_butch_femme(self):
        for index in range(1, len(self.merge_data) - 1):
            # print(get_merge_data[index])
            if self.merge_data[index]['high_value'] > self.merge_data[index - 1]['high_value'] and \
                    self.merge_data[index]['high_value'] > self.merge_data[index + 1]['high_value']:
                self.butch_list.append([self.merge_data[index - 1], self.merge_data[index], self.merge_data[index + 1]])

            if self.merge_data[index]['low_value'] < self.merge_data[index - 1]['low_value'] and \
                    self.merge_data[index]['low_value'] < self.merge_data[index + 1]['low_value']:
                self.femme_list.append([self.merge_data[index - 1], self.merge_data[index], self.merge_data[index + 1]])

        # print(len(self.butch_list))
        # print(len(self.femme_list))

    def flag_butch_femme(self):
        butch_index = 0
        femme_index = 0
        for index, row in self.df.iterrows():
            if butch_index < len(self.butch_list):
                butch_date = self.butch_list[butch_index][1]["high_date"]
                if row["date"] == butch_date:
                    self.df.loc[index, "dd_flag"] = "butch"
                    butch_index += 1
                    self.markers_on.append(index)

            if femme_index < len(self.femme_list):
                femme_date = self.femme_list[femme_index][1]["low_date"]
                if row["date"] == femme_date:
                    self.df.loc[index, "dd_flag"] = "femme"
                    femme_index += 1
                    self.markers_on.append(index)

        # print(len(self.df))

    def _make_plot(self, df_, param):
        # l1 = plt.plot(self.df["date"], self.df["close"], 'r', label='close')
        # l2 = plt.plot(df_['date'], df_['price'], 'b', label='trend')
        plt.plot(self.df["date"], self.df["close"], 'r', df_['date'], df_[param], 'b')
        plt.savefig("result/tmp/test_v1.svg", format="svg")
        plt.show()

    def run(self):
        self.k_data_handle()
        self.get_butch_femme()
        self.flag_butch_femme()

        # df2 = self.df.dropna(how="any")

        plt.plot(self.df["date"], self.df["close"], '-rD', markevery=self.markers_on)
        plt.savefig("result/tmp/test_v1.svg", format="svg")
        plt.show()


if __name__ == '__main__':
    ChanBi(data_path="dataset/stock/sz.002044.csv").run()
