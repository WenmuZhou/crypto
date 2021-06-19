#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/6/19 20:16
# @Author   : Adolf
# @File     : technical_indications.py
# @Function  :


def cal_vol_weight_ma(df, time_period):
    return df.apply(lambda row: row["close"] * row["volume"], axis=1).rolling(
        time_period).mean() / df["volume"].rolling(time_period).mean()