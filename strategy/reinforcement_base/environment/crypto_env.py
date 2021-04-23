#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/4/22 14:06
# @Author   : Adolf
# @File     : crypto_env.py
# @Function  :
import gym
from gym import spaces


class CustomEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, arg1, arg2):
        super(CustomEnv, self).__init__()
