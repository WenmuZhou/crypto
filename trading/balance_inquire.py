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
from trading.UserInfo import api_key_dict, api_secret_dict

exchange = ccxt.binance()


def get_balance_inquire():
    res_msg = "======定时账户余额查询======"
    res_msg += "\n\n"
    now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # print(now_time.split(" ")[1][:2])
    balance_dict = {}
    with open("log/balance_value", "r") as f:
        for line in f.readlines():
            one_balance = line.strip().split(":")
            balance_dict[one_balance[0]] = float(one_balance[1])
    # print(now_time)
    if now_time.split(" ")[1][:2] == "00":
        write_file = True
    else:
        write_file = False
    if write_file:
        file = open("log/balance_value", "w")
    res_msg += "当前时间:{}\n\n".format(now_time)
    res_msg += "-------------------"
    res_msg += "\n\n"

    for api_name, api_key in api_key_dict.items():
        api_secret = api_secret_dict[api_name]
        exchange.apiKey = api_key
        exchange.secret = api_secret

        balance_my, max_value_coin, balance_my_value = get_balance_info(exchange)

        if api_name not in balance_dict:
            with open("log/balance_value", "a") as f:
                f.write(api_name)
                f.write(":")
                f.write(str(balance_my_value))
                f.write("\n")

            balance_dict[api_name] = balance_my_value

        today_rate_of_return = (balance_my_value - balance_dict[api_name]) / balance_dict[api_name]

        res_msg += "账户所有人:{}\n\n账户余额:{:.2f}元\n\n目前持仓:{}\n\n今日收益率:{:.2f}%\n\n".format(
            api_name, balance_my_value, max_value_coin, today_rate_of_return * 100)
        if write_file:
            file.write(api_name)
            file.write(":")
            file.write(str(balance_my_value))
            file.write("\n")
        res_msg += "-------------------"
        res_msg += "\n\n"

    post_msg_to_dingtalk(msg=res_msg)
    if write_file:
        file.close()
    print(res_msg)


if __name__ == '__main__':
    get_balance_inquire()
