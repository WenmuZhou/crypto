# ！/usr/bin/env python
# -*- coding:utf-8 -*-
import ccxt

exchange = ccxt.binance()

balance = exchange.fetch_balance()
for coin in balance["info"]["balances"]:
    if float(coin["free"]) != 0 or float(coin["locked"]) != 0:
        print(coin)

