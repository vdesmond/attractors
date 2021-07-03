#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3  # noqa: F401
import numpy as np
from matplotlib import animation
from mpl_toolkits.mplot3d.art3d import Line3DCollection

from attractors import data
from attractors.utils.base import ATTRACTOR_PARAMS
from attractors.utils.colortable import get_continuous_cmap
from attractors.utils.des import DES
from attractors.utils.video import ffmpeg_video

try:
    import importlib.resources as pkg_resources
except ImportError:
    import importlib_resources as pkg_resources

# * load theme
raw_themes_data = pkg_resources.open_text(data, "themes.json")
themes = json.load(raw_themes_data)


class Attractor(DES):

    bgcolor = None
    palette = None
    fig, ax = None, None

    def __init__(self, initial_coord, attractor, **kwargs):
        self.attr = ATTRACTOR_PARAMS[attractor]
        params = {
            self.attr["params"][i]: kwargs.get(
                self.attr["params"][i], self.attr["default_params"][i]
            )
            for i in range(len(self.attr["params"]))
        }
        super(Attractor, self).__init__(initial_coord, attractor, params)

    def __eq__(self, other):
        if not isinstance(other, Attractor):
            return NotImplemented
        return self.attractor == other.attractor

    @classmethod
    def set_theme(cls, theme, bgcolor, palette):
        if all(v is None for v in [theme, bgcolor, palette]):
            cls.bgcolor = "#000000"
            cls.palette = "jet"
        elif all(v is None for v in [bgcolor, palette]) and theme is not None:
            palette_temp = list(theme.values())
            palette_temp.remove(theme["background"])
            cls.bgcolor = theme["background"]
            cls.palette = palette_temp
        else:
            if bgcolor is not None:
                cls.bgcolor = bgcolor
            if palette is not None:
                cls.palette = palette

    @classmethod
    def set_figure(cls, width, height, dpi):
        cls.fig = plt.figure(figsize=(width, height), dpi=dpi)
        cls.ax = cls.fig.add_axes([0, 0, 1, 1], projection="3d")
        cls.ax.axis("off")

        cls.fig.set_facecolor(cls.bgcolor)
        cls.ax.set_facecolor(cls.bgcolor)

        if isinstance(cls.palette, str):
            cls.cmap = plt.cm.get_cmap(cls.palette)
        else:
            cls.cmap = get_continuous_cmap(cls.palette)

    @classmethod
    def set_limits(cls, xlim, ylim, zlim):
        cls.ax.set_xlim(xlim)
        cls.ax.set_ylim(ylim)
        cls.ax.set_zlim(zlim)

    @classmethod
    def _wrap_set(cls, objs, kwargs):

        assert all(
            x == objs[0] for x in objs
        ), "All objects must be of the same attractor type"

        try:
            theme = themes[kwargs.get("theme")]
        except KeyError:
            theme = None

        Attractor.set_theme(
            theme,
            bgcolor=kwargs.get("bgcolor", None),
            palette=kwargs.get("palette", None),
        )
        Attractor.set_figure(
            width=kwargs.get("width", 16),
            height=kwargs.get("width", 9),
            dpi=kwargs.get("dpi", 120),
        )

        attr = ATTRACTOR_PARAMS[objs[0].attractor]
        Attractor.set_limits(
            xlim=kwargs.get("xlim", attr["xlim"]),
            ylim=kwargs.get("ylim", attr["ylim"]),
            zlim=kwargs.get("zlim", attr["zlim"]),
        )

    @classmethod
    def set_animate_multipoint(cls, *objs, **kwargs):

        Attractor._wrap_set(objs, kwargs)
        colors = cls.cmap(np.linspace(0, 1, len(objs)))

        lines = sum(
            [
                cls.ax.plot([], [], [], "-", c=c, linewidth=1, antialiased=True)
                for c in colors
            ],
            [],
        )
        pts = sum([cls.ax.plot([], [], [], "o", c=c) for c in colors], [])

        def init():
            for line, pt in zip(lines, pts):
                line.set_data_3d([], [], [])
                pt.set_data_3d([], [], [])
            return lines + pts

        def update(i):
            i = i % len(objs[0].X)
            for line, pt, k in zip(lines, pts, objs):
                line.set_data_3d(k.X[:i], k.Y[:i], k.Z[:i])
                pt.set_data_3d(k.X[i], k.Y[i], k.Z[i])
            cls.ax.view_init(0.005 * i, 0.05 * i)
            return lines + pts

        points = len(max(objs).X)
        return update, points, init

    @classmethod
    def set_animate_gradient(cls, obj, **kwargs):

        Attractor._wrap_set([obj], kwargs)

        line = Line3DCollection([], cmap=cls.cmap)
        cls.ax.add_collection3d(line)

        (pt,) = cls.ax.plot([], [], [], "o")
        line.set_array(np.array(obj.Z))
        colors = line.to_rgba(obj.Z)

        def init():
            line.set_segments([])
            pt.set_data_3d([], [], [])
            return line, pt

        def update(i):
            i = i % len(obj.X)
            pts = (
                np.array([obj.X[:i], obj.Y[:i], obj.Z[:i]])
                .transpose()
                .reshape(-1, 1, 3)
            )
            segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
            line.set_segments(segs)
            pt.set_data_3d([obj.X[i]], [obj.Y[i]], [obj.Z[i]])
            pt.set_color(colors[i])
            cls.ax.view_init(0.005 * i, 0.05 * i)
            return line, pt

        points = len(obj.X)
        return update, points, init

    @classmethod
    def animate(cls, update, points, init=None, **kwargs):
        if kwargs.get("live", False):
            _ = animation.FuncAnimation(
                cls.fig,
                update,
                init_func=init,
                interval=1000 / kwargs.get("fps", 60),
                blit=False,
            )
            plt.show()
        else:
            ffmpeg_video(
                cls.fig,
                update,
                points,
                kwargs.get("fps", 60),
                kwargs.get("outf", "output.mp4"),
            )
