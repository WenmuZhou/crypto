#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/4/19 15:06
# @Author   : Adolf
# @File     : turn_trade.py
# @Function  :
from trading.trade_strategy.base_trading import BasisTrading


class TurnTrade(BasisTrading):
    def strategy_trade(self, params):
        coin_list = params.get("coin_list", ["BTC", "ETH"])
        momentum_days = params.get("momentum_days", 5)
        time_periods = params.get("time_periods", "4h")

        coin_mom = {}
        for coin_name in coin_list:
            df = self.get_data(coin_name, time_periods, momentum_days * 2)
            df = self.cal_technical_index(df, momentum_days)
            coin_mom[coin_name] = df.tail(1)["coin_mom"].item()

        max_value = max(coin_mom.values())
        print("coin_mom:", coin_mom)
        for keys, values in coin_mom.items():
            if values == max_value:
                # print(keys, values)
                now_style = keys
                if max_value <= 0:
                    now_style = "USDT"
        print("now style:", now_style)
        return now_style


if __name__ == '__main__':
    auto_trade = TurnTrade(post_to_ding_talk=True)
    # auto_trade.trading_main(coin_list=["BTC", "ETH", "ADA", "DOT", "ONT", "UNI", "BNB"], user="wxt", time_periods="4h",
    # momentum_days=5)
    #
    # auto_trade.trading_main(
    #     coin_list=["EOS", "ANT", "DOT", "CHZ", "ADA", "UNI", "DOGE", "FIL", "CAKE", "ONT", "TLM", "BNB"], user="wenmu",
    #     time_periods="4h", momentum_days=5)
    #     auto_trade.trading_main(coin_list=["DOT", "ADA"], user="zuol", time_periods="4h", data_limit=10, momentum_days=5)
    # auto_trade.trading_main(coin_list=["BTC", "ETH", "CAKE", "BCH", "ETC"], user="shuig", time_periods="1d",
    #                         momentum_days=20)
    # auto_trade.trading_main(coin_list=["BTC", "ETH", "BNB", "DOT", "UNI", "CAKE", "ADA"], user="shengl",
    #                         time_periods="1d", momentum_days=10)
    # auto_trade.trading_main(coin_list=["BTC", "ETH", "XRP", "BNB"], user="yanjx", time_periods="1d",
    #                         momentum_days=10)
    auto_trade.trading_main(coin_list=["ETH", "FIL", "LTC", "ETC", "BCH", "BAT",
                                       "XRP", "DOT", "KSM", "CAKE", "LINK", "UNI",
                                       "CHZ", "DOGE", "BAKE", "MATIC"], user="nan",
                            time_periods="30m",
                            momentum_days=46)
