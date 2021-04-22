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
    # 构建自己的线上交易策略
    def strategy_trade(self, params):
        """

        :param params: 输入一些需要的参数
            coin_name: 操作的币种
            long_ma: 长期均线的时间周期
            short_ma: 短期均线的时间周期
            time_periods: 查看多少时间的
        :return:
            返回策略选定的需要买入的币种
        """
        coin_name = params.get("coin_name", "BTC")
        long_ma = params.get("long_ma", 10)
        short_ma = params.get("short_ma", 5)
        time_periods = params.get("time_periods", "4h")

        df = self.get_data(coin_name, time_periods, long_ma * 2)
        df["short_ma"] = talib.SMA(df["close"], timeperiod=short_ma)
        df["long_ma"] = talib.SMA(df["close"], timeperiod=long_ma)
        # print(df)
        print(df.tail(1))

        if df.tail(1)["short_ma"].item() > df.tail(1)["long_ma"].item():
            now_style = "REEF"
        else:
            now_style = "USDT"
        return now_style


if __name__ == '__main__':
    auto_trade = TwoMATrade(post_to_ding_talk=False)
    auto_trade.trading_main(coin_name="REEF", long_ma=45, short_ma=5, user="feip", time_periods="4h")
