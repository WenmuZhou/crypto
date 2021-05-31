#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/5/31 13:20
# @Author   : Adolf
# @File     : webstock_binance.py
# @Function  :
import websocket


def on_message(ws, message):
    print(message)


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


websocket.enableTrace(True)
ws = websocket.WebSocketApp("wss://stream.binance.com:9443/ws/btcusdt@trde",
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close)
ws.run_forever(sslopt={"check_hostname": False})
