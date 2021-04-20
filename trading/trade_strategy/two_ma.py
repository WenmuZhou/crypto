# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @Project : crypto
# @Date    : 2021/4/17 18:28
# @Author  : Adolf
# @File    : two_ma.py
# @Function:
import talib
from trading.trade_strategy.base_trading import BasisTrading


class TwoMATrade(BasisTrading):
    def strategy_trade(self, coin_name, long_ma, short_ma, time_periods, user):
        df = self.get_data(coin_name, time_periods, long_ma * 2)
        df["short_ma"] = talib.SMA(df["close"], timeperiod=short_ma)
        df["long_ma"] = talib.SMA(df["close"], timeperiod=long_ma)
        print(df)
        if df.tail(1)["short_ma"].item() > df.tail(1)["long_ma"].item():
            now_style = "REEF"
        else:
            now_style = "USDT"
        return now_style


if __name__ == '__main__':
    auto_trade = TwoMATrade()
    auto_trade.trading_main(coin_name="REEF", long_ma=45, short_ma=5, user="feip", time_periods="4h")
