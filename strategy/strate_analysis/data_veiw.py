#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/4/29 13:22
# @Author   : Adolf
# @File     : data_veiw.py
# @Function  :
import pandas as pd

pd.set_option('expand_frame_repr', False)

data_path = "/root/adolf/dataset/d/sh.600570.csv"

df = pd.read_csv(data_path)
print(df)
