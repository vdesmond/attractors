#!/usr/bin/env python
# -*- coding: utf-8 -*-
import matplotlib.colors as mcolors
import numpy as np


def hex_to_rgb(value):
    value = value.strip("#")
    lv = len(value)
    rgb_vals = tuple(
        int(value[i : i + lv // 3], 16) for i in range(0, lv, lv // 3)  # noqa: E203
    )
    return [v / 256 for v in rgb_vals]


def get_continuous_cmap(hex_list, float_list=None):
    rgb_list = [hex_to_rgb(i) for i in hex_list]
    if float_list:
        pass
    else:
        float_list = list(np.linspace(0, 1, len(rgb_list)))

    cdict = dict()
    for num, col in enumerate(["red", "green", "blue"]):
        col_list = [
            [float_list[i], rgb_list[i][num], rgb_list[i][num]]
            for i in range(len(float_list))
        ]
        cdict[col] = col_list
    cmp = mcolors.LinearSegmentedColormap("my_cmp", segmentdata=cdict, N=256)
    return cmp
