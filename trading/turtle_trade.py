# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @Project : crypto
# @Date    : 2021/4/16 22:36
# @Author  : Adolf
# @File    : turtle_trade.py
# @Function:
import ccxt
import pandas as pd
import datetime
from trading.utils import post_msg_to_dingtalk, get_balance_info
from trading.laboratory import api_key_dict, api_secret_dict

exchange = ccxt.binance()

exchange.apiKey = api_key_dict["yujl"]
exchange.secret = api_secret_dict["yujl"]
