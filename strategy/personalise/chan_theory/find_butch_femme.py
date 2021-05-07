#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/5/6 19:18
# @Author   : Adolf
# @File     : find_butch_femme.py
# @Function  :
from strategy.personalise.chan_theory.K_data_handle import get_merge_data

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
b_p = 0
f_p = 0

line_bi = []

while b_p < len(butch_list) - 1 or f_p < len(femme_list) - 1:
    b_t = butch_list[b_p][1][0]
    f_t = femme_list[f_p][1][0]
    if b_t > f_t:
        # 目前是底分型
        f_p += 1
        if len(line_bi) == 0:
            line_bi.append([femme_list[f_p], "f"])
        else:
            pre_point = line_bi[-1]
            # print('11111111')
            # if pre_point
            # print(line_bi)
    else:
        # 目前是顶分型
        b_p += 1
        if len(line_bi) == 0:
            line_bi.append([butch_list[b_p], "b"])
        else:
            # print('222222222')
            pre_point_flag = line_bi[-1][1]
            print(pre_point)
            if pre_point_flag == "f":
                pass
            else:
                pass
            break

# print(line_bi)