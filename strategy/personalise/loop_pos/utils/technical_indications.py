#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/6/19 20:16
# @Author   : Adolf
# @File     : technical_indications.py
# @Function  :
import talib


# 计算成交量加权平均移动线
def cal_vol_weight_ma(df, time_period=5):
    return df.apply(lambda row: row["close"] * row["volume"], axis=1).rolling(
        time_period).mean() / df["volume"].rolling(time_period).mean()


# 计算波动率的平均移动线
def cal_atr(df, time_period=14):
    pass


# 计算同花顺标注的多空点
def cal_ths_ls(df):
    df['var1'] = (100 - (90 * (df.high.rolling(21).max() - df.close) / (df.high.rolling(
        21).max() - df.low.rolling(21).min())))
    df["var2"] = df["var1"]
    df["var3_tmp"] = 100 * (df.high.rolling(6).max() - df.close) / (df.high.rolling(
        6).max() - df.low.rolling(6).min())
    df["var3"] = 100 - df.var3_tmp.rolling(34).mean()

    df["var4"] = df.var3.rolling(6).mean()
