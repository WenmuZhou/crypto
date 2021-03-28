# ！/usr/bin/env python
# -*- coding:utf-8 -*-
import os

for path, dir_list, file_list in os.walk("dataset"):
    print(file_list)
    for file in file_list:
        if ".csv" in file:
            new_name = file.split(".")[0].upper()
            os.rename(os.path.join(path, file), os.path.join(path, new_name + ".csv"))
