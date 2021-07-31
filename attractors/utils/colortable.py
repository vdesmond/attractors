#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#  Copyright (c) 2021. Vignesh M
#  This file colortable.py, part of the attractors package is licensed under the MIT license.
#  See LICENSE.md in the project root for license information.
# ------------------------------------------------------------------------------

"""Module that handles palettes and colormaps
"""


from typing import List

import matplotlib.colors as mcolors
import numpy as np


def hex_to_rgb(value: str) -> List[float]:
    """Converts hex to normalized rgb colours

    Args:
        value (str): string of 6 characters representing a hex colour

    Returns:
        list[float]: rgb color list
    """
    value = value.strip("#")
    lv = len(value)
    rgb_vals = tuple(
        int(value[i : i + lv // 3], 16) for i in range(0, lv, lv // 3)  # noqa: E203
    )
    return [v / 256 for v in rgb_vals]


def get_continuous_cmap(hex_list: List[str]) -> mcolors.LinearSegmentedColormap:
    """Creates and returns a color map from a given hex list.

    Args:
        hex_list (list[str]): list of hex code strings

    Returns:
        matplotlib.colors.LinearSegmentedColormap: Colormap of given hex list.
    """
    rgb_list = [hex_to_rgb(i) for i in hex_list]
    float_list = list(np.linspace(0, 1, len(rgb_list)))

    cdict = {}
    for num, col in enumerate(["red", "green", "blue"]):
        col_list = [
            [float_list[i], rgb_list[i][num], rgb_list[i][num]]
            for i in range(len(float_list))
        ]
        cdict[col] = col_list
    return mcolors.LinearSegmentedColormap("my_cmp", segmentdata=cdict, N=256)
