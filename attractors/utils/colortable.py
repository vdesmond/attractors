#!/usr/bin/env python
# -*- coding: utf-8 -*-
import matplotlib.colors as mcolors
import numpy as np


def hex_to_rgb(value):
    """
    Converts hex to normalized rgb colours

    Args:
        value (str): string of 6 characters representing a hex colour

    Returns:

    """
    value = value.strip("#")
    lv = len(value)
    rgb_vals = tuple(
        int(value[i : i + lv // 3], 16) for i in range(0, lv, lv // 3)  # noqa: E203
    )
    return [v / 256 for v in rgb_vals]


def get_continuous_cmap(hex_list, float_list=None):
    """
    Creates and returns a color map from a given hex list. If float_list
    is not provided, colour map graduates linearly between each color
    in hex_list. If float_list is provided, each color in hex_list is
    mapped to the respective location in float_list.

    Args:
        hex_list (list[str]): list of hex code strings
        float_list (list[float], optional): list of floats between 0 and 1,
            same length as hex_list. Must start with 0 and end with 1. Defaults to None.

    Returns:
        LinearSegmentedColormap: Colormap of given hex list.
    """
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
