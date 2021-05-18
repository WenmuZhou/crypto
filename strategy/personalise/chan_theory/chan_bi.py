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
        del df['amount'], df['turn'], df['pctChg'], df['adjustflag']
        self.df = df[-1000:]
        self.df.reset_index(drop=True, inplace=True)
        self.merge_data = []
        self.butch_list = []
        self.femme_list = []
        self.markers_on = []

        self.line_bi = []

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

    def merge_butch_femme(self):
        del self.df["dd_flag"]
        self.markers_on.clear()
        b_p = 0  # 顶
        f_p = 0  # 底

        while b_p < len(self.butch_list) - 1 or f_p < len(self.femme_list) - 1:
            b_t = self.butch_list[b_p][1]['high_date']
            f_t = self.femme_list[f_p][1]['low_date']
            # print(1111, b_t)
            if b_t > f_t:
                # 目前是底分型
                if len(self.line_bi) == 0:
                    self.line_bi.append(
                        [self.femme_list[f_p][1]['low_date'], "f", self.femme_list[f_p][1]['low_value']])
                else:
                    pre_point_flag = self.line_bi[-1][1]
                    # 上一个是顶分型
                    if pre_point_flag == "b":
                        now_femme = self.femme_list[f_p]
                        pre_butch = self.butch_list[b_p - 1]
                        # print('当前的底:', now_butch)
                        # print("上一个的顶", pre_butch)
                        if now_femme[0]['low_date'] > pre_butch[2]['high_date'] and \
                                now_femme[1]["low_value"] < min(one_k['low_value'] for one_k in pre_butch) and \
                                max(one_k['high_value'] for one_k in now_femme) < pre_butch[1]['high_value']:
                            self.line_bi.append([now_femme[1]["low_date"], "f", now_femme[1]["low_value"]])
                        else:
                            if len(self.line_bi) > 1 and now_femme[1]["low_value"] < self.line_bi[-2][2]:
                                self.line_bi.pop()
                                self.line_bi.pop()
                                self.line_bi.append([now_femme[1]["low_date"], "f", now_femme[1]["low_value"]])
                    # 上一个节点也是底分型
                    else:
                        now_femme = self.femme_list[f_p]
                        pre_femme = self.line_bi[-1]
                        if now_femme[1]["low_value"] < pre_femme[2]:
                            self.line_bi.pop()
                            self.line_bi.append([now_femme[1]["low_date"], "f", now_femme[1]["low_value"]])
                f_p += 1
            else:
                # 目前是顶分型
                # if b_t == "2020-07-09":
                #     print('----')
                if len(self.line_bi) == 0:
                    self.line_bi.append([self.butch_list[b_p][1][0], "b", self.butch_list[b_p][1][1]])
                else:
                    pre_point_flag = self.line_bi[-1][1]
                    # 上一个节点是底
                    if pre_point_flag == "f":
                        now_butch = self.butch_list[b_p]
                        pre_femme = self.femme_list[f_p - 1]
                        # print('当前的顶:', now_butch)
                        # print("上一个的底:", pre_femme)
                        if now_butch[0]["high_date"] > pre_femme[2]["low_date"] and \
                                now_butch[1]["high_value"] > max(one_k["high_value"] for one_k in pre_femme) and \
                                min(one_k["low_value"] for one_k in now_butch) > pre_femme[1]["low_value"]:
                            self.line_bi.append([now_butch[1]["high_date"], "b", now_butch[1]["high_value"]])

                        else:
                            if len(self.line_bi) > 1 and now_butch[1]["high_value"] > self.line_bi[-2][2]:
                                # print(b_p)
                                # print(line_bi)
                                self.line_bi.pop()
                                self.line_bi.pop()
                                self.line_bi.append([now_butch[1]["high_date"], "b", now_butch[1]["high_value"]])
                    # 上一个节点也是顶
                    else:
                        now_butch = self.butch_list[b_p]
                        pre_butch = self.line_bi[-1]
                        if now_butch[1]["high_value"] > pre_butch[2]:
                            self.line_bi.pop()
                            self.line_bi.append([now_butch[1]["high_date"], "b", now_butch[1]["high_value"]])
                    # break
                b_p += 1

    def add_bi_markers_on(self):
        line_bi_index = 0
        for index, row in self.df.iterrows():
            if line_bi_index == len(self.line_bi):
                break
            if row["date"] == self.line_bi[line_bi_index][0]:
                self.df.loc[index, 'flag_bf'] = self.line_bi[line_bi_index][1]
                self.df.loc[index, 'flag_id'] = line_bi_index
                self.markers_on.append(index)
                line_bi_index += 1

    def cut_butch_femme(self):
        last_index = -5
        for index, row in self.df.iterrows():
            # print(index, row)
            if not pd.isna(row["flag_bf"]):
                if index - last_index < 5:
                    if row["flag_bf"] == "b":
                        pre_high = self.df[self.df["flag_id"] == (row["flag_id"] - 2)].high.item()
                        if row["flag_id"] > 1 and row["high"] > pre_high:
                            self.df.loc[last_index, "flag_bf"] = "gan"
                            self.df.loc[self.df["flag_id"] == (row["flag_id"] - 2), "flag_bf"] = "gan"
                            last_index = index
                        else:
                            self.df.loc[index, "flag_bf"] = "gan"

                    if row["flag_bf"] == "f":
                        pre_low = self.df[self.df["flag_id"] == (row["flag_id"] - 2)].low.item()
                        if row["flag_id"] > 1 and row["low"] < pre_low:
                            self.df.loc[last_index, "flag_bf"] = "gan"
                            self.df.loc[self.df["flag_id"] == (row["flag_id"] - 2), "flag_bf"] = "gan"
                            last_index = index
                        else:
                            self.df.loc[index, "flag_bf"] = "gan"
                else:
                    last_index = index
            # break

        # exit()
        last_state = "p"
        last_index = -1
        for index, row in self.df.iterrows():
            if row["flag_bf"] == "b" and row["flag_bf"] == last_state:
                if self.df.loc[index, "high"] > self.df.loc[last_index, "high"]:
                    self.df.loc[last_index, 'flag_bf'] = "gan"
                    last_index = index
                else:
                    self.df.loc[index, 'flag_bf'] = "gan"
            elif row["flag_bf"] == "f" and row["flag_bf"] == last_state:
                if self.df.loc[index, "low"] < self.df.loc[last_index, "low"]:
                    self.df.loc[last_index, "flag_bf"] = "gan"
                    last_index = index
                else:
                    self.df.loc[index, 'flag_bf'] = "gan"
            elif row["flag_bf"] == "b" or row["flag_bf"] == "f":
                last_state = row["flag_bf"]
                last_index = index
            else:
                continue
        # # exit()
        self.df.loc[self.df["flag_bf"] == "b", "price"] = self.df["high"]
        self.df.loc[self.df["flag_bf"] == "f", "price"] = self.df["low"]

        # df2 = self.df.dropna(how="any")
        # print(self.df)

    def run(self, save_path, make_plot=False):
        self.k_data_handle()
        self.get_butch_femme()
        self.flag_butch_femme()
        self.merge_butch_femme()
        self.add_bi_markers_on()
        self.cut_butch_femme()

        df2 = self.df.dropna(how="any")
        # print(self.line_bi)
        # exit()
        if make_plot:
            plt.plot(self.df["date"], self.df["high"], '-r', df2['date'], df2['price'], 'b')
        plt.savefig(save_path, format="svg")
        plt.show()
        return self.df


if __name__ == '__main__':
<<<<<<< HEAD
    stock_id = "002044"
    ChanBi(data_path="dataset/stock/" + stock_id + ".csv").run(save_path="result/chan_bi/" + stock_id + ".svg",
                                                               make_plot=True)
=======
    stock_id = "600570"
    res_df = ChanBi(data_path="dataset/stock/" + stock_id + ".csv").run(save_path="result/chan_bi/" + stock_id + ".svg",
                                                                        make_plot=False)
    res_df.to_csv("result/chan_" + stock_id + ".csv", index=False)
>>>>>>> 04cf20b... update data
