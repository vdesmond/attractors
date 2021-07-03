#!/usr/bin/env python
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3  # noqa: F401
import numpy as np
from mpl_toolkits.mplot3d.art3d import Line3DCollection

from attractors.utils.colortable import get_continuous_cmap
from attractors.utils.des import DES
from attractors.utils.video import ffmpeg_video


def animate_gradient(
    attractor,
    init_coord,
    attr_params,
    xlim,
    ylim,
    zlim,
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
    ax.axis("off")
    fig.set_facecolor(bgcolor)
    ax.set_facecolor(bgcolor)

    vect = DES(init_coord, attractor, attr_params)
    try:
        rk = getattr(vect, des)
        if des == "rk2":
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
    colors = line.to_rgba(vect.Z)

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
