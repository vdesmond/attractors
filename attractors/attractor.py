#!/usr/bin/env python
# -*- coding: utf-8 -*-
from attractors.utils.des import DES
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3  # noqa: F401
import numpy as np
from matplotlib import animation
from attractors.utils.base import ATTRACTOR_PARAMS
import json
from attractors import data
try:
    import importlib.metadata as metadata
    import importlib.resources as pkg_resources
except ImportError:
    import importlib_resources as pkg_resources
    import importlib_metadata as metadata

# * load theme
raw_themes_data = pkg_resources.open_text(data, "themes.json")
themes = json.load(raw_themes_data)


class Attractors(DES):
    def __init__(self, initial_coord, attractor, params):
        super(Attractors, self).__init__(initial_coord, attractor, params)

    def __eq__(self,other):
        if not isinstance(other, Attractors):
                return NotImplemented
        return self.attractor == other.attractor

    @staticmethod 
    def set_theme(kwargs):

        try:
            theme = themes[kwargs.get('theme')]
        except KeyError:
            theme = None
        bgcolor = kwargs.get('bgcolor', None)
        palette = kwargs.get('cmap', None)

        if all(v is None for v in [theme, bgcolor, palette]):
            bgcolor = "#000000"
            palette = "jet"
        elif all(v is None for v in [bgcolor, palette]) and theme is not None:
            palette_temp = list(theme.values())
            palette_temp.remove(theme["background"])
            bgcolor = theme["background"]
            palette = palette_temp
        else:
            pass

    @staticmethod 
    def animate_sim(*objs, **kwargs):

        assert all(x==objs[0] for x in objs), "All objects must be of the same attractor type"
        


        width = kwargs.get('width',"16")
        height = kwargs.get('width',"9")
        dpi = kwargs.get('dpi',"120")


        fig = plt.figure(figsize=(width, height), dpi=dpi)
        ax = fig.add_axes([0, 0, 1, 1], projection="3d")
        ax.axis("off")
        fig.set_facecolor(bgcolor)
        ax.set_facecolor(bgcolor)

        attr = ATTRACTOR_PARAMS[objs[0].attractor]
        xlim = kwargs.get('xlim', attr["xlim"])
        ylim = kwargs.get('ylim', attr["ylim"])
        zlim = kwargs.get('zlim', attr["zlim"])

        
        if isinstance(palette, str):
            cmap = plt.cm.get_cmap(palette)
        else:
            cmap = get_continuous_cmap(palette)

        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
        ax.set_zlim(zlim)