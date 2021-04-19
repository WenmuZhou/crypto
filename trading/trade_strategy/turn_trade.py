#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/4/19 15:06
# @Author   : Adolf
# @File     : turn_trade.py
# @Function  :
from trading.trade_strategy.base_trading import BasisTrading


class TurnTrade(BasisTrading):
    def __init__(self,
                 exchange_name="binance",
                 title="rich",
                 token="8392f247561974cf01f63efc77bfeb814c70a00453aee8eb26c405081af03dbe"):
        super(TurnTrade, self).__init__(exchange_name=exchange_name, title=title, token=token)

    def strategy_trade(self, coin_list, momentum_days, user, time_periods):
        coin_mom = {}
        for coin_name in coin_list:
            df = self.get_data(coin_name, time_periods, momentum_days * 2)
            df = self.cal_technical_index(df, momentum_days)
            coin_mom[coin_name] = df.tail(1)["coin_mom"].item()

        max_value = max(coin_mom.values())
        for keys, values in coin_mom.items():
            if values == max_value:
                # print(keys, values)
                now_style = keys
                if max_value <= 0:
                    now_style = "USDT"

        return now_style

# if __name__ == '__main__':
#     auto_trade = TurnTrade()
#     auto_trade.trading_main(coin_list=["BTC", "ETH", "ADA", "DOT", "ONT", "UNI", "BNB"], user="wxt", time_periods="4h",
#                             data_limit=10, momentum_days=5)
#
#     auto_trade.trading_main(
#         coin_list=["EOS", "ANT", "DOT", "CHZ", "ADA", "UNI", "DOGE", "FIL", "CAKE", "ONT", "TLM", "BNB"], user="wenmu",
#         time_periods="4h", data_limit=10, momentum_days=5)
#     auto_trade.trading_main(coin_list=["DOT", "ADA"], user="zuol", time_periods="4h", data_limit=10, momentum_days=5)
