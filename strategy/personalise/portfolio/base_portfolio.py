#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/6/21 13:26
# @Author   : Adolf
# @File     : base_portfolio.py
# @Function  :
import os
import pandas as pd

pd.set_option("expand_frame_repr", False)

dataset_dir = '/root/adolf/dataset/stock/handle_stock/mom_res'
df = pd.read_csv(os.path.join(dataset_dir, "sh.600570.csv"))
print(df.head())
