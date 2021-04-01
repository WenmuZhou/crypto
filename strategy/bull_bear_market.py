# ！/usr/bin/env python
# -*- coding:utf-8 -*-
import pandas as pd
import talib

pd.set_option("expand_frame_repr", False)
pd.set_option("display.max_rows", 1000)


def cal_bull_bear(coin_name):
    df = pd.read_csv("dataset/day/" + coin_name + ".csv")
    del df['high'], df['low'], df['vol']

    for i in [1, 3, 5, 10, 20, 30]:
        df[str(i) + 'day_pct'] = df['close'].pct_change(i)
        df[str(i) + 'day_pct'] = df[str(i) + 'day_pct'].shift(-i)

    for i in [3, 5, 10, 20, 30, 60]:
        df[str(i) + '_ma'] = talib.SMA(df["close"], timeperiod=i)
        # df['3day_pct'] = df['close'].pct_change(3)
    # df.dropna(subset=['1day_pct'],inplace=True)
    df = df.dropna(how="any")
    df.reset_index(drop=True, inplace=True)
    res = []
    for i in [1, 3, 5, 10, 20, 30]:
        for j in [3, 5, 10, 20, 30, 60]:
            df["sum_pct"] = df.loc[df["close"] > df[str(j) + '_ma'], str(i) + 'day_pct']
            tmp_df = df.dropna(how="any")
            mean_df = tmp_df.mean(axis=0)
            one_res = [coin_name, str(j) + '_ma', str(i) + 'day_pct', mean_df["sum_pct"]]
            res.append(one_res)
    # print(mean_df['sum_pct']*100)
    return res


# sum_pct = tmp_df.loc[len(tmp_df)-1,"sum_pct"]
# print(tmp_df)
coin_list = ["BNB", "BTC", "DOT", "EOS", "ETH", "FIL", "LTC", "XRP"]
all_res = []
for coin_name in coin_list:
    res_pct = cal_bull_bear(coin_name)
    all_res += res_pct

res_df = pd.DataFrame(all_res, columns=["币名", "周期线", "时间", "回报率"])
res_df.to_csv("result/牛熊分割线.csv", encoding="gbk", index=False)
# print(res_df)
