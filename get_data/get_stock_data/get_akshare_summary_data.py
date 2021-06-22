#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/6/22 9:28
# @Author   : Adolf
# @File     : get_akshare_summary_data.py
# @Function  :
import akshare as ak

#上交所总貌
stock_sse_summary_df = ak.stock_sse_summary()
print(stock_sse_summary_df)

#深交所总貌
stock_szse_summary_df = ak.stock_szse_summary(date="20210621")
print(stock_szse_summary_df)

#上交所每日概况
stock_sse_deal_daily_df = ak.stock_sse_deal_daily(date="20210621")
print(stock_sse_deal_daily_df)