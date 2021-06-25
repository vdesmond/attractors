#!/usr/bin/env python
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3  # noqa: F401
import numpy as np
from mpl_toolkits.mplot3d.art3d import Line3DCollection

from attractors.utils.attr import ATTRACTOR_PARAMS
from attractors.utils.colortable import get_continuous_cmap
from attractors.utils.runge_kutta import RK
from attractors.utils.video import ffmpeg_video


def animate_gradient(
    attractor,
    width,
    height,
    dpi,
    bgcolor,
    palette,
    sim_time,
    points,
    des,
    rk2_method,
    fps,
    outf,
):

    fig = plt.figure(figsize=(width, height), dpi=dpi)
    ax = fig.add_axes([0, 0, 1, 1], projection="3d")
    
    fig.set_facecolor(bgcolor)
    ax.set_facecolor(bgcolor)

    ax.w_xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.w_yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.w_zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))

    ax.w_xaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
    ax.w_yaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
    ax.w_zaxis.line.set_color((1.0, 1.0, 1.0, 0.0))

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])

    attr = ATTRACTOR_PARAMS[attractor]
    init_coord = attr["init_coord"]
    attr_params = dict(zip(attr["params"], attr["default_params"]))
    xlim = attr["xlim"]
    ylim = attr["ylim"]
    zlim = attr["zlim"]

    vect = RK(init_coord, attractor, attr_params)
    try:
        rk = getattr(vect, des)
        if des == "RK2":
            rk(0, sim_time, points, rk2_method)
        else:
            rk(0, sim_time, points)
    except AttributeError as e:
        raise Exception(f"Integrator Error. {des} is not an valid integrator") from e

    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_zlim(zlim)

    if isinstance(palette, str):
        cmap = plt.cm.get_cmap(palette)
    else:
        cmap = get_continuous_cmap(palette)

    line = Line3DCollection([], cmap=cmap)
    ax.add_collection3d(line)

    (pt,) = ax.plot([], [], [], "o")

    def init():
        line.set_segments([])
        pt.set_data_3d([], [], [])

    init()

    line.set_array(np.array(vect.Y))
    colors = line.to_rgba(vect.Y)

    def update(frame):

        i = frame % len(vect.X)
        pts = (
            np.array([vect.X[:i], vect.Y[:i], vect.Z[:i]]).transpose().reshape(-1, 1, 3)
        )
        segs = np.concatenate([pts[:-1], pts[1:]], axis=1)

        line.set_segments(segs)

        pt.set_data_3d([vect.X[i]], [vect.Y[i]], [vect.Z[i]])
        pt.set_color(colors[i])

        ax.view_init(0.005 * i, 0.05 * i)

    ffmpeg_video(fig, update, points, fps, outf)
