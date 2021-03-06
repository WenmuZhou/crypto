#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/5/19 10:56
# @Author   : Adolf
# @File     : time_30min.py
# @Function  :
from trading.trade_strategy.turn_trade import TurnTrade

auto_trade = TurnTrade()
try:
    auto_trade.trading_main(
        coin_list=['BTC', 'ETH', 'EOS', 'FIL', 'LTC', 'ETC', 'BCH', 'BAT', 'XRP', 'DOT', 'KSM', 'LINK', 'ADA',
                   'UNI', 'CHZ', 'DOGE', 'MATIC'],
        user="nan",
        time_periods="30m",
        momentum_days=47)
except Exception as e:
    print(e)
    print('nan bug')
