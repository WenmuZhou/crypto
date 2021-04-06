#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/4/6 9:58
# @Author  : Adolf
# @File    : two_ma_pro.py
import os
import pandas as pd

data_dir = "dataset/day/"
data_list = os.listdir(data_dir)

for data_name in data_list:
    print(data_name)
    df = pd.read_csv(os.path.join(data_dir,data_name))
    print(df)
    break