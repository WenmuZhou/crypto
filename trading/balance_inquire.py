#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/4/16 13:50
# @Author   : Adolf
# @File     : balance_inquire.py
# @Function  :
import ccxt
import datetime
from trading.utils import get_balance_info, post_msg_to_dingtalk
from trading.laboratory import api_key_dict, api_secret_dict

exchange = ccxt.binance()

coin_list = ["BTC", "ETH", "XRP", "EOS", "ANT", "DOT", "CHZ", "ADA", "UNI", "DOGE", "FIL", "CAKE", "ONT",
             "TLM", "BNB"]

res_msg = "======定时账户余额查询======"
res_msg += "\n\n"
res_msg += "当前时间:{}\n\n".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
res_msg += "-------------------"
res_msg += "\n\n"

for api_name, api_key in api_key_dict.items():
    api_secret = api_secret_dict[api_name]
    exchange.apiKey = api_key
    exchange.secret = api_secret

    balance_my, max_value_coin, balance_my_value = get_balance_info(coin_list, exchange)

    res_msg += "账户所有人:{}\n\n账户余额：{:.2f}万元\n\n目前持仓：{}\n\n".format(
        api_name, balance_my_value, max_value_coin)
    res_msg += "-------------------"
    res_msg += "\n\n"

post_msg_to_dingtalk(msg=res_msg)
