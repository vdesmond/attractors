#!/usr/bin/env python
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3  # noqa: F401
import numpy as np
from matplotlib import animation

from attractors.utils.colortable import get_continuous_cmap
from attractors.utils.des import DES
from attractors.utils.video import ffmpeg_video


def animate_simulation(
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
    n,
    des,
    live,
    rk2_method,
    fps,
    outf,
):

    fig = plt.figure(figsize=(width, height), dpi=dpi)
    ax = fig.add_axes([0, 0, 1, 1], projection="3d")
    ax.axis("off")
    fig.set_facecolor(bgcolor)
    ax.set_facecolor(bgcolor)

    init_coords = [init_coord] + [
        init_coord + np.random.normal(0, 0.01, 3) for _ in range(n - 1)
    ]

    attractor_vects = [DES(xyz, attractor, attr_params) for xyz in init_coords]

    for vect in attractor_vects:
        try:
            rk = getattr(vect, des)
            if des == "rk2":
                rk(0, sim_time, points, rk2_method)
            else:
                rk(0, sim_time, points)
        except AttributeError as e:
            raise Exception(
                f"Integrator Error. {des} is not an valid integrator"
            ) from e

    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_zlim(zlim)

    if isinstance(palette, str):
        cmap = plt.cm.get_cmap(palette)
    else:
        cmap = get_continuous_cmap(palette)

    colors = cmap(np.linspace(0, 1, len(init_coords)))

    lines = sum(
        [ax.plot([], [], [], "-", c=c, linewidth=1, antialiased=True) for c in colors],
        [],
    )
    pts = sum([ax.plot([], [], [], "o", c=c) for c in colors], [])

    trail = int(0.9 * points)

    def init():
        for line, pt in zip(lines, pts):
            line.set_data_3d([], [], [])
            pt.set_data_3d([], [], [])
        return lines + pts

    def update(i):
        i = i % len(attractor_vects[0].X)
        for line, pt, k in zip(lines, pts, attractor_vects):
            if i > trail:
                line.set_data_3d(
                    k.X[i - trail : i],  # noqa: E203
                    k.Y[i - trail : i],  # noqa: E203
                    k.Z[i - trail : i],  # noqa: E203
                )
            else:
                line.set_data_3d(k.X[:i], k.Y[:i], k.Z[:i])
            pt.set_data_3d(k.X[i], k.Y[i], k.Z[i])
        ax.view_init(0.005 * i, 0.05 * i)
        return lines + pts

    if live:
        _ = animation.FuncAnimation(
            fig, update, init_func=init, interval=1000 / fps, blit=False
        )
        plt.show()
    else:
        ffmpeg_video(fig, update, points, fps, outf)
