'''
邢不行 | 量化小讲堂系列文章
《Python量化 + 数字货币 + 轮动 = 4年1000倍【邢不行】》
https://www.bilibili.com/video/BV1mX4y137BY
有任何问题或获取更多量化文章，请联系邢不行个人微信：xbx2626
'''
import pandas as pd
import numpy as np
from function import *
import matplotlib.pyplot as plt

pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
pd.set_option('display.max_rows', 5000)  # 最多显示数据的行数

# 读取数据
df_coin1 = pd.read_csv(
    '../../../../../../Library/Containers/com.tencent.xinWeChat/Data/Library/Application Support/com.tencent.xinWeChat/2.0b4.0.9/5ceade320df788a8c0b9a221edaaa3ad/Message/MessageTemp/3005d887ed74e648cc6c832892128ed1/File/数字货币轮动/BTCUSD-1d.csv',
    encoding='gbk', parse_dates=['candle_end_time'])
df_coin2 = pd.read_csv(
    '../../../../../../Library/Containers/com.tencent.xinWeChat/Data/Library/Application Support/com.tencent.xinWeChat/2.0b4.0.9/5ceade320df788a8c0b9a221edaaa3ad/Message/MessageTemp/3005d887ed74e648cc6c832892128ed1/File/数字货币轮动/ETHUSD-1d.csv',
    encoding='gbk', parse_dates=['candle_end_time'])

# 设置参数
trade_rate = 2.5 / 1000  # 千分之2.5的交易费用远高于市场平均水平
momentum_days = 20  # 计算多少天的涨跌幅

# 计算两种币每天的涨跌幅pct
df_coin1['coin1_pct'] = df_coin1['close'].pct_change(1)
df_coin2['coin2_pct'] = df_coin2['close'].pct_change(1)
# 重命名行
df_coin1.rename(columns={'open': 'coin1_open', 'close': 'coin1_close'}, inplace=True)
df_coin2.rename(columns={'open': 'coin2_open', 'close': 'coin2_close'}, inplace=True)
# 合并数据
df = pd.merge(left=df_coin1[['candle_end_time', 'coin1_open', 'coin1_close', 'coin1_pct']], left_on=['candle_end_time'],
              right=df_coin2[['candle_end_time', 'coin2_open', 'coin2_close', 'coin2_pct']],
              right_on=['candle_end_time'], how='left')
# 计算N日的涨跌幅momentum
df['coin1_mom'] = df['coin1_close'].pct_change(periods=momentum_days)
df['coin2_mom'] = df['coin2_close'].pct_change(periods=momentum_days)
# 轮动条件
df.loc[df['coin1_mom'] > df['coin2_mom'], 'style'] = 'coin1'
df.loc[df['coin1_mom'] < df['coin2_mom'], 'style'] = 'coin2'
# 相等时维持原来的仓位。
df['style'].fillna(method='ffill', inplace=True)
# 收盘才能确定风格，实际的持仓pos要晚一天。
df['pos'] = df['style'].shift(1)
# 删除持仓为nan的天数
df.dropna(subset=['pos'], inplace=True)
# 数字货币从17年开始回测
df = df[df['candle_end_time'] >= pd.to_datetime('20170101')]
# 计算策略的整体涨跌幅strategy_pct
df.loc[df['pos'] == 'coin1', 'strategy_pct'] = df['coin1_pct']
df.loc[df['pos'] == 'coin2', 'strategy_pct'] = df['coin2_pct']

# 调仓时间
df.loc[df['pos'] != df['pos'].shift(1), 'trade_time'] = df['candle_end_time']
# 将调仓日的涨跌幅修正为开盘价买入涨跌幅
df.loc[(df['trade_time'].notnull()) & (df['pos'] == 'coin1'), 'strategy_pct_adjust'] = df['coin1_close'] / (
        df['coin1_open'] * (1 + trade_rate)) - 1
df.loc[(df['trade_time'].notnull()) & (df['pos'] == 'coin2'), 'strategy_pct_adjust'] = df['coin2_close'] / (
        df['coin2_open'] * (1 + trade_rate)) - 1
df.loc[df['trade_time'].isnull(), 'strategy_pct_adjust'] = df['strategy_pct']
# 扣除卖出手续费
df.loc[(df['trade_time'].shift(-1).notnull()), 'strategy_pct_adjust'] = (1 + df[
    'strategy_pct']) * (1 - trade_rate) - 1
del df['strategy_pct'], df['style']

df.reset_index(drop=True, inplace=True)
# 计算净值
df['coin1_net'] = df['coin1_close'] / df['coin1_close'][0]
df['coin2_net'] = df['coin2_close'] / df['coin2_close'][0]
df['strategy_net'] = (1 + df['strategy_pct_adjust']).cumprod()

# 评估策略的好坏
res = evaluate_investment(df, 'strategy_net', time='candle_end_time')
print(res)

# 绘制图形
plt.plot(df['candle_end_time'], df['strategy_net'], label='strategy')
plt.plot(df['candle_end_time'], df['coin1_net'], label='coin1_net')
plt.plot(df['candle_end_time'], df['coin2_net'], label='coin2_net')
plt.show()

# 保存文件
print(df.tail(10))
df.to_csv('数字货币轮动.csv', encoding='gbk', index=False)
