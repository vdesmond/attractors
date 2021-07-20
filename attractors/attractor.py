#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from random import shuffle

import matplotlib
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3  # noqa: F401
import numpy as np
from matplotlib import animation
from more_itertools import peekable
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

    _update_func = None
    _points = None
    _init_func = None

    def __init__(self, attractor, **kwargs):
        self.attr = ATTRACTOR_PARAMS[attractor]
        self.init_coord = kwargs.get("init_coord", self.attr["init_coord"])
        self.params = {
            self.attr["params"][i]: kwargs.get(
                self.attr["params"][i], self.attr["default_params"][i]
            )
            for i in range(len(self.attr["params"]))
        }
        super(Attractor, self).__init__(attractor, self.init_coord, self.params)

    def __eq__(self, other):
        if not isinstance(other, Attractor):
            return NotImplemented
        return self.attractor == other.attractor

    @staticmethod
    def list_themes():
        return themes

    @staticmethod
    def list_des():
        des_methods = set(dir(DES.__mro__[0])) - set(dir(DES.__mro__[1]))
        return [x for x in des_methods if not x.startswith("_")]

    @staticmethod
    def list_attractors():
        return list(ATTRACTOR_PARAMS.keys())

    @staticmethod
    def list_params(attr):
        return ATTRACTOR_PARAMS[attr]["params"]

    @classmethod
    def set_theme(cls, theme, bgcolor, palette):
        if all(v is None for v in [theme, bgcolor, palette]):
            cls.bgcolor = "#000000"
            cls.palette = "jet"
        elif all(v is None for v in [bgcolor, palette]) and theme is not None:
            palette_temp = list(theme.values())
            palette_temp.remove(theme["background"])
            palette_temp.insert(0, palette_temp.pop(-1))
            shuffle(palette_temp)
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
            x.peek().attractor == objs[0].peek().attractor for x in objs
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

        attr = ATTRACTOR_PARAMS[objs[0].peek().attractor]
        Attractor.set_limits(
            xlim=kwargs.get("xlim", attr["xlim"]),
            ylim=kwargs.get("ylim", attr["ylim"]),
            zlim=kwargs.get("zlim", attr["zlim"]),
        )

    @classmethod
    def set_animate_multipoint(cls, *objs, **kwargs):

        objs = [peekable(obj) for obj in objs]

        Attractor._wrap_set(objs, kwargs)
        colors = cls.cmap(np.linspace(0, 1, len(objs)))

        linekwargs = kwargs.get("linekwargs", {})
        pointkwargs = kwargs.get("pointkwargs", {})

        lines = sum(
            [
                cls.ax.plot([], [], [], "-", c=c, antialiased=True, **linekwargs)
                for c in colors
            ],
            [],
        )
        pts = sum(
            [cls.ax.plot([], [], [], "o", c=c, **pointkwargs) for c in colors], []
        )

        def init():
            for line, pt in zip(lines, pts):
                line.set_data_3d([], [], [])
                pt.set_data_3d([], [], [])
            return lines + pts

        maxlen = len(max([obj.peek() for obj in objs], key=len))

        def update(i):
            for line, pt, k in zip(lines, pts, objs):
                s = next(k, None)
                if not s:
                    continue
                if i == maxlen - 1:
                    plt.close(
                        line.axes.figure
                    )  # Manually closing figure after all attractors have been animated
                line.set_data_3d(
                    np.hstack(
                        (
                            np.array(line.get_data_3d()),
                            np.atleast_2d(np.array([s.X, s.Y, s.Z])).T,
                        )
                    )
                )
                pt.set_data_3d(s.X, s.Y, s.Z)

            cls.ax.view_init(
                kwargs.get("elevationrate", 0.005) * i,
                kwargs.get("azimuthrate", 0.05) * i,
            )

            return lines + pts

        cls._update_func = update
        cls._init_func = init
        cls._points = maxlen
        return cls

    @classmethod
    def set_animate_gradient(cls, obj, **kwargs):

        obj = peekable(obj)
        Attractor._wrap_set([obj], kwargs)

        # Find a way to skip these steps? (need the full list for color array)
        objlist = []
        for s in obj:
            objlist.append([s.X, s.Y, s.Z])
        objlist = np.array(objlist)

        linekwargs = kwargs.get("linekwargs", {})
        pointkwargs = kwargs.get("pointkwargs", {})

        line = Line3DCollection([], cmap=cls.cmap, **linekwargs)
        cls.ax.add_collection3d(line)

        val = {"X": 0, "Y": 1, "Z": 2}
        colorarray = objlist[:, val[kwargs.get("gradientaxis", "Z")]]

        (pt,) = cls.ax.plot([], [], [], "o", **pointkwargs)
        line.set_array(np.array(colorarray))
        colors = line.to_rgba(colorarray)

        del colorarray

        def init():
            line.set_segments([])
            pt.set_data_3d([], [], [])
            return line, pt

        def update(i):

            pts = np.array(objlist[:i]).reshape(-1, 1, 3)
            segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
            line.set_segments(segs)
            pt.set_data_3d([objlist[i, 0]], [objlist[i, 1]], [objlist[i, 2]])
            pt.set_color(colors[i])
            cls.ax.view_init(
                kwargs.get("elevationrate", 0.005) * i,
                kwargs.get("azimuthrate", 0.05) * i,
            )
            return line, pt

        points = len(objlist)
        cls._update_func = update
        cls._init_func = init
        cls._points = points
        return cls

    @classmethod
    def animate(cls, **kwargs):
        if kwargs.get("live", False):
            anim = animation.FuncAnimation(
                cls.fig,
                cls._update_func,
                init_func=cls._init_func,
                interval=1000 / kwargs.get("fps", 60),
                blit=False,
            )
            if kwargs.get("show", True):
                plt.show()
            else:
                return anim
        else:
            matplotlib.use("Agg")
            ffmpeg_video(
                cls.fig,
                cls._update_func,
                cls._points,
                kwargs.get("fps", 60),
                kwargs.get("outf", "output.mp4"),
            )

    @classmethod
    def plot_gradient(cls, index, obj, **kwargs):
        obj = peekable(obj)
        Attractor._wrap_set([obj], kwargs)

        objlist = [[s.X, s.Y, s.Z] for s in obj]
        objlist = np.array(objlist)

        linekwargs = kwargs.get("linekwargs", {})
        pointkwargs = kwargs.get("pointkwargs", {})

        line = Line3DCollection([], cmap=cls.cmap, **linekwargs)
        cls.ax.add_collection3d(line)

        val = {"X": 0, "Y": 1, "Z": 2}
        colorarray = objlist[:, val[kwargs.get("gradientaxis", "Z")]]

        (pt,) = cls.ax.plot([], [], [], "o", **pointkwargs)
        line.set_array(np.array(colorarray))
        colors = line.to_rgba(colorarray)

        pts = np.array(objlist[:index]).reshape(-1, 1, 3)
        segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
        line.set_segments(segs)
        pt.set_data_3d([objlist[index, 0]], [objlist[index, 1]], [objlist[index, 2]])
        pt.set_color(colors[index])
        cls.fig.canvas.draw()
        return cls.ax

    @classmethod
    def plot_multipoint(cls, index, *objs, **kwargs):

        objs = [peekable(obj) for obj in objs]

        Attractor._wrap_set(objs, kwargs)
        colors = cls.cmap(np.linspace(0, 1, len(objs)))

        linekwargs = kwargs.get("linekwargs", {})
        pointkwargs = kwargs.get("pointkwargs", {})

        lines = sum(
            (
                cls.ax.plot([], [], [], "-", c=c, antialiased=True, **linekwargs)
                for c in colors
            ),
            [],
        )

        pts = sum(
            (cls.ax.plot([], [], [], "o", c=c, **pointkwargs) for c in colors), []
        )

        for line, pt, k in zip(lines, pts, objs):
            tx, ty, tz = [], [], []
            for s in k:
                if s.ts == index:
                    break
                tx += [s.X]
                ty += [s.Y]
                tz += [s.Z]

            line.set_data_3d(tx, ty, tz)
            pt.set_data_3d(s.X, s.Y, s.Z)
        cls.fig.canvas.draw()
        return cls.ax
