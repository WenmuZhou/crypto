# ！/usr/bin/env python
# -*- coding:utf-8 -*-
import ccxt
# import talib

exchange = ccxt.binance()

exchange.apiKey = "e3cDWMh8N1uugwePjZK0OLZ73dMCl45kX7kIbniN9kjx42r5UtBAGs1S6JKvEXiu"
exchange.secret = "F6OShDNksFqTqCqD8mGbAEmi7sDubGWxHakra3nA8xVn3RWbw9qsDqNMi75OhNVG"

# data = exchange.fetch_ticker("LTC/USDT")
# print(data)

# data2 = exchange.fetch_ohlcv("BTC/USDT", timeframe="15m", limit=3)
# print(data2)

balance = exchange.fetch_balance()
# print(balance)
# print(balance)
for coin in balance["info"]["balances"]:
    if float(coin["free"]) != 0 or float(coin["locked"]) != 0:
        print(coin)

# order_info = exchange.create_limit_buy_order(symbol="BTC/USDT", amount=0.01, price=1)
