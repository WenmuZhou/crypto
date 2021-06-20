#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/6/19 20:33
# @Author   : Adolf
# @File     : signal_point.py
# @Function  :

# 指标一上穿指标二
def up_cross(df, arg1, arg2, name="long"):
    df[name] = False
    df.loc[(df[arg1] > df[arg2]) & (
            df[arg1].shift(1) <= df[arg2].shift(1)), name] = True


# 指标一下穿指标二
def down_cross(df, arg1, arg2, name="short"):
    df[name] = False
    df.loc[(df[arg1] < df[arg2]) & (
            df[arg1].shift(1) >= df[arg2].shift(1)), name] = True


# 指标向上拐头
def up(df, arg2, name):
    df[name] = False
    df.loc[(df[arg2] > df[arg2].shift(1)) & (
            df[arg2].shift(2) > df[arg2].shift(1)), name] = True


# 指标向下拐头
def down(df, arg2, name):
    df[name] = False
    df.loc[(df[arg2] < df[arg2].shift(1)) & (
            df[arg2].shift(2) < df[arg2].shift(1)), name] = True


# 判断当前的持仓状态
def get_current_pos(df, buy_point="long", sell_point="short", name="pos"):
    df.loc[df[buy_point], name] = True
    df.loc[df[sell_point], name] = False
    df[name].fillna(method='pad', inplace=True)
    df[name].fillna(False,inplace=True)
