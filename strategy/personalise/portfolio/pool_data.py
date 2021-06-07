#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/6/7 19:08
# @Author   : Adolf
# @File     : pool_data.py
# @Function  :
import os
import shutil

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
stock_list = os.listdir(stock_dir)
print(len(stock_list))
