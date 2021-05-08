#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/5/6 19:18
# @Author   : Adolf
# @File     : find_butch_femme.py
# @Function  :
from strategy.personalise.chan_theory.K_data_handle import get_merge_data, df

# print(get_merge_data)
butch_list = []
femme_list = []
for index in range(1, len(get_merge_data) - 1):
    # print(get_merge_data[index])
    if get_merge_data[index][1] > get_merge_data[index - 1][1] and \
            get_merge_data[index][1] > get_merge_data[index + 1][1]:
        butch_list.append([get_merge_data[index - 1], get_merge_data[index], get_merge_data[index + 1]])

    if get_merge_data[index][2] < get_merge_data[index - 1][2] and \
            get_merge_data[index][2] < get_merge_data[index + 1][2]:
        femme_list.append([get_merge_data[index - 1], get_merge_data[index], get_merge_data[index + 1]])

# print(butch_list)
# print("=" * 100)
# print(femme_list)
b_p = 0  # 顶
f_p = 0  # 底

line_bi = []

while b_p < len(butch_list) - 1 or f_p < len(femme_list) - 1:
    b_t = butch_list[b_p][1][0]
    f_t = femme_list[f_p][1][0]
    if b_t > f_t:
        # 目前是底分型
        if len(line_bi) == 0:
            line_bi.append([femme_list[f_p][1][0], "f", femme_list[f_p][1][2]])
        else:
            pre_point_flag = line_bi[-1][1]
            # 上一个是顶分型
            if pre_point_flag == "b":
                now_femme = femme_list[f_p]
                pre_butch = butch_list[b_p - 1]
                # print('当前的底:', now_butch)
                # print("上一个的顶", pre_butch)
                if now_femme[0][0] > pre_butch[2][0] and now_femme[1][2] < min(one_k[2] for one_k in pre_butch) and \
                        max(one_k[1] for one_k in now_femme) < pre_butch[1][1]:
                    line_bi.append([now_femme[1][0], "f", now_femme[1][2]])
            # 上一个节点也是底分型
            else:
                now_femme = femme_list[f_p]
                pre_femme = femme_list[f_p - 1]
                if now_femme[1][2] < pre_femme[1][2]:
                    line_bi.pop()
                    line_bi.append([now_femme[1][0], "f", now_femme[1][2]])
        f_p += 1
    else:
        # 目前是顶分型
        if len(line_bi) == 0:
            line_bi.append([butch_list[b_p][1][0], "b", butch_list[b_p][1][1]])
        else:
            pre_point_flag = line_bi[-1][1]
            # 上一个节点是底
            if pre_point_flag == "f":
                now_butch = butch_list[b_p]
                pre_femme = femme_list[f_p - 1]
                # print('当前的顶:', now_butch)
                # print("上一个的底:", pre_femme)
                if now_butch[0][0] > pre_femme[2][0] and now_butch[1][1] > max(one_k[1] for one_k in pre_femme) and \
                        min(one_k[2] for one_k in now_butch) > pre_femme[1][2]:
                    line_bi.append([now_butch[1][0], "b", now_butch[1][1]])
            # 上一个节点也是顶
            else:
                now_butch = butch_list[b_p]
                pre_butch = butch_list[b_p - 1]
                if now_butch[1][1] > pre_butch[1][1]:
                    line_bi.pop()
                    line_bi.append([now_butch[1][0], "b", now_butch[1][1]])
            # break
        b_p += 1

# print(df)
# print(line_bi)

line_bi_index = 0
for index, row in df.iterrows():
    if line_bi_index == len(line_bi) - 1:
        break
    if row["date"] == line_bi[line_bi_index][0]:
        df.loc[index, 'flag'] = line_bi[line_bi_index][1]
        line_bi_index += 1

print(df)
df.to_csv("result/hs_stock.csv")
