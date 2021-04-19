#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/4/19 17:18
# @Author   : Adolf
# @File     : time_1d.py
# @Function  :
from trading.trade_strategy.turn_trade import TurnTrade
from trading.trade_strategy.turtle_trade import turtle_trade_v2

auto_trade = TurnTrade()
auto_trade.trading_main(coin_list=["BTC", "ETH"], user="nan", time_periods="1d", momentum_days=10)

turtle_trade_v2(coin_list=["BTC"], user="yujl")
