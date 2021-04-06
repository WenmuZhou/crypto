# ！/usr/bin/env python
# -*- coding:utf-8 -*-
import time
import pandas as pd
from backtest.base_function import evaluate_investment
import matplotlib.pyplot as plt

pd.set_option("expand_frame_repr", False)
pd.set_option("display.max_rows", 1000)

df_coin1 = pd.read_csv("dataset/day/BTC.csv")
df_coin2 = pd.read_csv("dataset/day/LTC.csv")

trade_rate = 2 / 1000
# trade_rate = 0
momentum_days = 20

df_coin1['coin1_pct'] = df_coin1['close'].pct_change(1)
df_coin2['coin2_pct'] = df_coin2['close'].pct_change(1)

df_coin1.rename(columns={'open': 'coin1_open', 'close': 'coin1_close'}, inplace=True)
df_coin2.rename(columns={'open': 'coin2_open', 'close': 'coin2_close'}, inplace=True)
# print(df_coin1)

df = pd.merge(left=df_coin1[['time_stamp', 'coin1_open', 'coin1_close', 'coin1_pct']], left_on=['time_stamp'],
              right=df_coin2[['time_stamp', 'coin2_open', 'coin2_close', 'coin2_pct']],
              right_on=['time_stamp'], how='left')

df['coin1_mom'] = df['coin1_close'].pct_change(periods=momentum_days)
df['coin2_mom'] = df['coin2_close'].pct_change(periods=momentum_days)

df.loc[df['coin1_mom'] > df['coin2_mom'], 'style'] = 'coin1'
df.loc[df['coin1_mom'] < df['coin2_mom'], 'style'] = 'coin2'
df.loc[(df['coin1_mom'] < 0) & (df['coin2_mom'] < 0), 'style'] = 'empty'

df['style'].fillna(method='ffill', inplace=True)
# 收盘才能确定风格，实际的持仓pos要晚一天。
df['pos'] = df['style'].shift(1)
# 删除持仓为nan的天数
df.dropna(subset=['pos'], inplace=True)

df.loc[df['pos'] == 'coin1', 'strategy_pct'] = df['coin1_pct']
df.loc[df['pos'] == 'coin2', 'strategy_pct'] = df['coin2_pct']

# print(df)

# 调仓时间
df.loc[df['pos'] != df['pos'].shift(1), 'trade_time'] = df['time_stamp']
# # 将调仓日的涨跌幅修正为开盘价买入涨跌幅
df.loc[(df['trade_time'].notnull()) & (df['pos'] == 'coin1'), 'strategy_pct_adjust'] = df['coin1_close'] / (
        df['coin1_open'] * (1 + trade_rate)) - 1
df.loc[(df['trade_time'].notnull()) & (df['pos'] == 'coin2'), 'strategy_pct_adjust'] = df['coin2_close'] / (
        df['coin2_open'] * (1 + trade_rate)) - 1
df.loc[df['trade_time'].isnull(), 'strategy_pct_adjust'] = df['strategy_pct']
# # 扣除卖出手续费
df.loc[(df['trade_time'].shift(-1).notnull()), 'strategy_pct_adjust'] = (1 + df[
    'strategy_pct']) * (1 - trade_rate) - 1

df['strategy_pct_adjust'].fillna(value=0.0, inplace=True)
del df['strategy_pct'], df['style']
#
df.reset_index(drop=True, inplace=True)
# # 计算净值
df['coin1_net'] = df['coin1_close'] / df['coin1_close'][0]
df['coin2_net'] = df['coin2_close'] / df['coin2_close'][0]
df['strategy_net'] = (1 + df['strategy_pct_adjust']).cumprod()

# df['time_stamp'] = df['time_stamp'].apply(lambda x: int(time.mktime(time.strptime(x, "%Y-%m-%d %H:%M:%S")) * 1000))
df['time_stamp'] = df['time_stamp'].apply(lambda x: int(time.mktime(time.strptime(x, "%Y-%m-%d")) * 1000))

# 评估策略的好坏
res = evaluate_investment(df, 'strategy_net', time='time_stamp')
print(res)
#
# # 绘制图形
plt.plot(df['time_stamp'], df['strategy_net'], label='strategy')
plt.plot(df['time_stamp'], df['coin1_net'], label='coin1_net')
plt.plot(df['time_stamp'], df['coin2_net'], label='coin2_net')
plt.show()
#
# # 保存文件
print(df.tail(10))
# df.to_csv('result/数字货币轮动.csv', index=False)
