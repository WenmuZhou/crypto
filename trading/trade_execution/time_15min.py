#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/5/11 16:38
# @Author   : Adolf
# @File     : time_15min.py
# @Function  :
from trading.trade_strategy.two_ma import TwoMATrade

auto_trade_ma = TwoMATrade()
try:
    auto_trade_ma.trading_main(coin_name="REEF", long_ma=25, short_ma=7, user="feip", time_periods="15m")
except Exception as e:
    print(e)
    print('feip bug')
