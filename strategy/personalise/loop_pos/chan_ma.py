#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/5/31 17:30
# @Author   : Adolf
# @File     : chan_ma.py
# @Function  :
import talib
import pandas as pd
from strategy.personalise.loop_pos.base_structure import TradeStructure

pd.set_option("expand_frame_repr", False)
pd.set_option("display.max_rows", 1000)


class ChanMA(TradeStructure):
    def __init__(self, data_path):
        super(ChanMA, self).__init__(data_path)

    def cal_technical_index(self):
        self.data = self.data[:1000]
        self.base_technical_index(ma_parm=(5, 10))
        self.data.dropna(inplace=True)
        self.data.reset_index(drop=True, inplace=True)

        self.data['diff'] = self.data.apply(lambda x: 100 * (x.MA5 - x.MA10) / min(x.MA5, x.MA10), axis=1)

        print(self.data)


if __name__ == '__main__':
    mawind = ChanMA(data_path="dataset/stock/600570_post.csv")
    mawind.cal_technical_index()
    # mawind(analyze_positions=True)
