#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/5/17 16:32
# @Author   : Adolf
# @File     : chan_zs.py
# @Function  :
import pandas as pd

pd.set_option("expand_frame_repr", False)

df = pd.read_csv("result/chan_002044.csv")
print(df)
