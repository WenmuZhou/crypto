#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/4/19 17:18
# @Author   : Adolf
# @File     : time_1d.py
# @Function  :
from trading.trade_strategy.turn_trade import TurnTrade
from trading.trade_strategy.turtle_trade import TurtleTrade

auto_trade = TurnTrade()
auto_trade.trading_main(coin_list=["BTC", "ETH"], user="nan", time_periods="1d", momentum_days=10)

auto_trade.trading_main(coin_list=["BTC", "ETH"], user="shuig", time_periods="1d", momentum_days=20)

auto_trade_v2 = TurtleTrade()
auto_trade_v2.trading_main(coin_name="BTC", user="yujl", upper_band=30, lower_band=20)
