#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/5/17 14:20
# @Author   : Adolf
# @File     : rename.py
# @Function  :
import os

data_dir = "dataset/"

for path, dir_list, file_list in os.walk(data_dir):
    for file_name in file_list:
        if "from" in file_name:
            new_file_name = file_name.replace(":", "-")
            print(new_file_name)
            print(os.path.join(path, file_name))
