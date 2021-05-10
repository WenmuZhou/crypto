#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/5/10 10:06
# @Author   : Adolf
# @File     : chan_bi.py
# @Function  :
import pandas as pd
import matplotlib.pyplot as plt


class ChanBi:
    def __init__(self, data_path):
        df = pd.read_csv(data_path)
        self.df = df[-1000:]
        self.merge_data = []
        # self.k_data_handle()

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
                pre_low_date = pre_dict["low_value"]
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

    def _make_plot(self, df_, param):
        plt.plot(self.df["date"], self.df["close"], "r", label="close")
        plt.savefig("result/tmp/test_v1.svg", format="svg")
        plt.show()

    def run(self):
        self.k_data_handle()
        print(self.merge_data)
        # self._make_plot()


if __name__ == '__main__':
    ChanBi(data_path="dataset/stock/sz.002044.csv").run()
