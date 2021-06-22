#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/6/22 9:54
# @Author   : Adolf
# @File     : get_akshare_stock_data.py
# @Function  :
import os.path

import ray
import pandas as pd
import akshare as ak
from get_data.get_stock_data.ch_eng_mapping import ch_eng_mapping_dict

pd.set_option("expand_frame_repr", False)
# 获取实时行情数据
stock_zh_a_spot_em_df = ak.stock_zh_a_spot_em()
stock_zh_a_spot_em_df.rename(columns=ch_eng_mapping_dict, inplace=True)
code_list = stock_zh_a_spot_em_df.code.to_list()

code_name_mapping = stock_zh_a_spot_em_df.set_index(['code'])['name'].to_dict()

ray.init()

error_code_list = []


@ray.remote
def get_one_stock_data(code):
    try:
        # 获取前复权数据
        stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol=code, adjust="qfq")
        stock_zh_a_hist_df.rename(columns=ch_eng_mapping_dict, inplace=True)
        # if len(stock_zh_a_hist_df) < 120:
        #     return 0
        stock_zh_a_hist_df["code"] = code
        stock_zh_a_hist_df["name"] = code_name_mapping[code]
        stock_zh_a_hist_df.to_csv(os.path.join("/data3/stock_data/stock_data/real_data/dongcai/qfq/", code + ".csv"),
                                  index=False)

        # 获取后复权数据
        stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol=code, adjust="hfq")
        stock_zh_a_hist_df.rename(columns=ch_eng_mapping_dict, inplace=True)
        # if len(stock_zh_a_hist_df) < 120:
        #     return 0
        stock_zh_a_hist_df["code"] = code
        stock_zh_a_hist_df["name"] = code_name_mapping[code]
        stock_zh_a_hist_df.to_csv(os.path.join("/data3/stock_data/stock_data/real_data/dongcai/hfq/", code + ".csv"),
                                  index=False)

        return 0
    except Exception as e:
        print(code)
        print(e)
        error_code_list.append(code)


futures = [get_one_stock_data.remote(code) for code in code_list]
ray.get(futures)

print("=" * 20)

