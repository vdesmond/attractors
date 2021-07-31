#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#  Copyright (c) 2021. Vignesh M
#  This file attractor.py, part of the attractors package is licensed under the MIT license.
#  See LICENSE.md in the project root for license information.
# ------------------------------------------------------------------------------
"""Main module for attractors package

Attributes:
    THEMES (dict): Contains theme palettes. Loaded from data/themes.json file.
"""
from __future__ import annotations

import importlib.resources as pkg_resources
import json
from random import shuffle
from typing import Iterator, List, Optional, Tuple, Union

import matplotlib
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d
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

# * load theme
THEMES = json.load(pkg_resources.open_text(data, "themes.json"))


class Attractor(DES):
    """Attractor class inherits from DES. It sets default arguments and handles the plotting and animation for both
    multipoint and gradient types.

    Attributes:
        attr (str): Attractor name
        init_coord (List[float]): Initial coordinate for the attractor
        params (Mapping[str, float]): Parameters of the attractor
    """

    #: str: Background color in hex
    bgcolor = None

    #: Union[str,List[str]]: Color palette for plotting. Takes either list of hex values or matplotlib cmap
    palette = None

    #: matplotlib.cmap) Matplotlib color map for figure (from palette)
    cmap = None

    #: matplotlib.figure.Figure: Matplotlib figure instance for Attractors class
    fig = None

    #: mpl_toolkits.mplot3d.Axes3D: Matplotlib axes instance for Attractors class
    ax = None

    _update_func = None
    _points = None
    _init_func = None

    def __init__(self, attractor: str, **kwargs):
        """Constructor for Attractors class

        Args:
            attractor (str): Attractor name
            **kwargs: See below

        Examples:

            A basic example for constructing an Attractors instance for "Lorenz"

                >>> attr = Attractor("lorenz", sigma = 5, rho = 28.5, init_coord = [0.2,0.1,0.1])

        Keyword Args:
            init_coord (List[float]): Initial coordinate for the attractor. Defaults to values from :mod:attractors.utils.data
            params (Mapping[str, float]): Parameters of the attractor. Defaults to values from :mod:attractors.utils.data
        """
        self.attr = ATTRACTOR_PARAMS[attractor]
        self.init_coord = np.array(kwargs.get("init_coord", self.attr["init_coord"]))
        self.params = {
            self.attr["params"][i]: kwargs.get(
                self.attr["params"][i], self.attr["default_params"][i]
            )
            for i in range(len(self.attr["params"]))
        }
        super(Attractor, self).__init__(
            attractor, np.copy(self.init_coord), self.params
        )

    def __eq__(self, other):
        if not isinstance(other, Attractor):
            return NotImplemented
        return self.attractor == other.attractor

    @staticmethod
    def list_themes() -> dict:
        """Static method to get themes as a JSON structured dict

        Returns:
            dict: JSON structured dict of all themes
        """
        return THEMES

    @staticmethod
    def list_des() -> List[str]:
        """Static method to get list of iterative ODE solvers that are available

        Returns:
            List[str]: List of iterative ODE solvers
        """
        des_methods = set(dir(DES.__mro__[0])) - set(dir(DES.__mro__[1]))
        return [x for x in des_methods if not x.startswith("_")]

    @staticmethod
    def list_attractors() -> List[str]:
        """Static method to get list of attractors that are implemented in the package

        Returns:
            List[str]: List of attractors
        """
        return list(ATTRACTOR_PARAMS.keys())

    @staticmethod
    def list_params(attr: str) -> List[str]:
        """Static method to get the parameters for a given attractor

        Args:
            attr (str): Attractor name

        Returns:
            List[str]: List of possible parameters
        """
        return ATTRACTOR_PARAMS[attr]["params"]

    @classmethod
    def set_theme(
        cls,
        theme: Optional[dict],
        bgcolor: Optional[str],
        palette: Optional[Union[str, List[str]]],
    ):
        """Class method that sets the background color and color palette for the matplotlib figure either via a theme
        or manually. If both theme and manual arguments are given, the manual arguments take precedence

        Args:
            theme (dict, optional): Theme palette in dict format containing colors and their respective hex values.
                Defaults to None.
            bgcolor (str, optional): Background color in hex. Defaults to None.
            palette (Union[str,List[str]], optional): Color palette in matplotlib cmap or list of hex values.
                Defaults to None.
        """
        if theme is not None:
            palette_temp = list(theme.values())
            palette_temp.remove(theme["background"])
            palette_temp.insert(0, palette_temp.pop(-1))
            shuffle(palette_temp)
            cls.bgcolor = theme["background"]
            cls.palette = palette_temp
        else:
            cls.bgcolor = "#000000"
            cls.palette = "jet"
        if bgcolor is not None:
            cls.bgcolor = bgcolor
        if palette is not None:
            cls.palette = palette

    @classmethod
    def set_figure(cls, width: float, height: float, dpi: float):
        """Class method to set figure size and dpi, and also set the background color and palette based on the
        current class attributes of the same name.

        Note:
            :func:`~attractor.Attractor.set_theme` must be called before this function

        Args:
            width (float): Width of the figure in inches
            height (float): Height of the figure in inches
            dpi (float): The resolution of the figure in dots-per-inch

        Raises:
            ValueError: When background color is NoneType or when palette is NoneType
        """
        cls.fig = plt.figure(figsize=(width, height), dpi=dpi)
        cls.ax = cls.fig.add_axes([0, 0, 1, 1], projection="3d")
        cls.ax.axis("off")

        if cls.bgcolor is None:
            raise ValueError("Background color cannot be NoneType")

        cls.fig.set_facecolor(cls.bgcolor)
        cls.ax.set_facecolor(cls.bgcolor)
        if cls.palette is None:
            raise ValueError("Palette cannot be NoneType")

        if isinstance(cls.palette, str):
            cls.cmap = plt.cm.get_cmap(cls.palette)
        else:
            cls.cmap = get_continuous_cmap(cls.palette)

    @classmethod
    def set_limits(
        cls,
        xlim: Tuple[float, float],
        ylim: Tuple[float, float],
        zlim: Tuple[float, float],
    ):
        """Class method to set figure limits for all 3 dimensions.

        Args:
            xlim (Tuple[float, float]): X-axis limits for the figure
            ylim (Tuple[float, float]): Y-axis limits for the figure
            zlim (Tuple[float, float]): Z-axis limits for the figure
        """
        cls.ax.set_xlim(xlim)
        cls.ax.set_ylim(ylim)
        cls.ax.set_zlim(zlim)

    @classmethod
    def _wrap_set(cls, objs: List[peekable[Iterator[DES]]], kwargs: dict):
        """Common function to call :func:`~attractor.Attractor.set_theme`, :func:`~attractor.Attractor.set_figure`,
        :func:`~attractor.Attractor.set_limits`.

        Note:
            Only for use with set_animate and plot functions.

        Args:
            objs (List[peekable]): Peekable version of generators returned from DES methods
            kwargs: all kwargs are just arguments of aforementioned set functions
        """

        assert all(
            x.peek().attractor == objs[0].peek().attractor for x in objs
        ), "All objects must be of the same attractor type"

        try:
            theme = THEMES[kwargs.get("theme")]
        except KeyError:
            theme = None

        Attractor.set_theme(
            theme, bgcolor=kwargs.get("bgcolor"), palette=kwargs.get("palette")
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
    def set_animate_multipoint(cls, *objs: Iterator[DES], **kwargs):
        """Class method to set the animation for multipoint

        Args:
            *objs: Variable length list of generators which yield DES
            **kwargs: See below

        Keyword Args:
            linekwargs (dict): Kwargs for matplotlib line plot for lines plotted in the figure. Defaults to {}
            pointkwargs (dict): Kwargs for matplotlib line plot for markers plotted in the figure. Defaults to {}
            elevationrate (float): Rate of change of elevation angle in animation per frame. Defaults to 0.005
            azimuthrate (float): Rate of change of azimuth angle in animation per frame. Defaults to 0.05

        Returns:
            Attractor: instance of the class
        """

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

        maxlen = len(max([obj.peek() for obj in objs], key=len))

        def init():
            for line, pt in zip(lines, pts):
                line.set_data_3d([], [], [])
                pt.set_data_3d([], [], [])
            return lines + pts

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
    def set_animate_gradient(cls, obj: Iterator[DES], **kwargs):
        """Class method to set the animation for gradient

        Args:
            obj: Generator which yields DES
            **kwargs: See below

        Keyword Args:
            linekwargs (dict): Kwargs for matplotlib line plot for lines plotted in the figure. Defaults to {}
            pointkwargs (dict): Kwargs for matplotlib line plot for markers plotted in the figure. Defaults to {}
            elevationrate (float): Rate of change of elevation angle in animation per frame. Defaults to 0.005
            azimuthrate (float): Rate of change of azimuth angle in animation per frame. Defaults to 0.05
            gradientaxis (str): Axis along which color gradient is applied. Defaults to "Z"

        Returns:
            Attractor: instance of the class
        """
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
            pts = np.array(objlist[:i]).reshape((-1, 1, 3))
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
    def animate(cls, **kwargs) -> Optional[matplotlib.animation.FuncAnimation]:
        """Classmethod that animates the figure after setting the animation parameters

        Example:

            Following example returns an FuncAnimation instance

                >>> inst = Attractor("dequan_li").rk3(0, 10, 10000)
                >>> x = Attractor.set_animate_gradient(inst).animate(live = True, show = False)

            Following example saves the animation to output MPEG4 encoded video file

                >>> inst = Attractor("dequan_li").rk3(0, 10, 10000)
                >>> x = Attractor.set_animate_gradient(inst).animate(outf="dequan_li.mp4")

        Note:
            :func:`~attractor.Attractor.set_animate_multipoint` or :func:`~attractor.Attractor.set_animate_gradient`,
            must be run before running this method.

        Keyword Args:
           fps (int): Frames per second for live plot/generated video. Defaults to 60
           live (bool): Flag to redirect plotting to FuncAnimation instead of piping to ffmpeg. Defaults to False
           show (bool): Flag to call `plt.show()` instead of returning FuncAnimation if `live = True`. Defaults to True
           outf (str): Filename of output video if generated. Defaults to "output.mp4"

        Returns:
            Optional[matplotlib.animation.FuncAnimation]: FuncAnimation instance if kwargs `live = True`, `show = False`
        """
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
    def plot_gradient(cls, obj: Iterator[DES], **kwargs) -> mpl_toolkits.mplot3d.Axes3D:
        """Class method to plot the attractor as gradient type

        Example:

            Following example generates a gradient plot at a particular index

                >>> inst = Attractor("dequan_li").rk3(0, 10, 10000)
                >>> ax = Attractor.plot_gradient(inst, index=8000)

        Args:
            obj: Generator which yields DES
            **kwargs: See below

        Keyword Args:
            index (int): Index to be plotted. Defaults to the final index plottable
            linekwargs (dict): Kwargs for matplotlib line plot for lines plotted in the figure. Defaults to {}
            pointkwargs (dict): Kwargs for matplotlib line plot for markers plotted in the figure. Defaults to {}
            gradientaxis (str): Axis along which color gradient is applied. Defaults to "Z"

        Returns:
            mpl_toolkits.mplot3d.Axes3D: Axes attribute of Attractor class
        """
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

        del colorarray

        index = kwargs.get("index", len(objlist) - 1)

        pts = np.array(objlist[:index]).reshape((-1, 1, 3))
        segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
        line.set_segments(segs)
        pt.set_data_3d([objlist[index, 0]], [objlist[index, 1]], [objlist[index, 2]])
        pt.set_color(colors[index])
        cls.fig.canvas.draw()
        return cls.ax

    @classmethod
    def plot_multipoint(
        cls, *objs: Iterator[DES], **kwargs
    ) -> mpl_toolkits.mplot3d.Axes3D:
        """Class method to plot the attractor as multipoint type

        Example:

            Following example generates a gradient plot at a particular index

                    >>> inst = Attractor("dequan_li").rk3(0, 10, 10000)
                    >>> ax = Attractor.plot_multipoint(inst, index=8000)

        Args:
            *objs: Variable length list of generators which yield DES
            **kwargs: See below

        Keyword Args:
            index (int): Index to be plotted. Defaults to the final index plottable
            linekwargs (dict): Kwargs for matplotlib line plot for lines plotted in the figure. Defaults to {}
            pointkwargs (dict): Kwargs for matplotlib line plot for markers plotted in the figure. Defaults to {}

        Returns:
            mpl_toolkits.mplot3d.Axes3D: Axes attribute of Attractor class
        """
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

        maxlen = len(max((obj.peek() for obj in objs), key=len))

        index = kwargs.get("index", maxlen - 1)

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
