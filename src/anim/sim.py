#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import mpl_toolkits.mplot3d.axes3d as p3
from matplotlib import animation
import matplotlib.pyplot as plt
import matplotlib as mpl
from numpy.lib.function_base import select
from src.utils.runge_kutta import RK
from src.utils.attractors import ATTRACTOR_PARAMS
from src.utils.colortable import get_continuous_cmap

def animate_simulation(attractor, width, height, dpi, bgcolor, palette, sim_time, points, n, integrator, rk2_method = "heun"):
    
    mpl.use("Qt5Cairo")
    fig = plt.figure(figsize=(width, height), dpi=dpi)
    ax = fig.add_axes([0, 0, 1, 1], projection='3d')
    ax.axis('off')
    fig.set_facecolor(bgcolor) 
    ax.set_facecolor(bgcolor)

    attr = ATTRACTOR_PARAMS[attractor]
    init_coord = np.array(attr["init_coord"], dtype='double')
    attr_params = dict(zip(attr["params"], attr["default_params"]))
    xlim = attr["xlim"]
    ylim = attr["ylim"]
    zlim = attr["zlim"]
    
    init_coords = [init_coord] + [init_coord + np.random.normal(0, 0.01, 3) for _ in range(n-1)]

    attractor_vects = [RK(xyz, attractor, attr_params) for xyz in init_coords]

    for vect in attractor_vects:
        try:
            rk = getattr(vect, integrator)
            if integrator == "RK2":
                rk(0, sim_time, points, rk2_method)
            else:
                rk(0, sim_time, points)
        except AttributeError as e:
            raise Exception(f"Integrator Error. {integrator} is not an valid integrator") from e
    
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_zlim(zlim)

    if isinstance(palette, str):
        cmap = plt.cm.get_cmap(palette)
    else:
        cmap = get_continuous_cmap(palette)
    
    colors = cmap(np.linspace(0, 1, len(init_coords)))

    lines = sum([ax.plot([], [], [], '-', c=c, linewidth=1, antialiased=True)
                for c in colors], [])
    points = sum([ax.plot([], [], [], 'o', c=c)
            for c in colors], [])                   

    def init():
        for line, pt in zip(lines, points):
            line.set_data_3d([], [], [])
            pt.set_data_3d([], [], [])
        return lines + points

    def animate(i):
        i = i % len(attractor_vects[0].X)
        for line, pt, k in zip(lines, points, attractor_vects):
            if i>15000:
                line.set_data_3d(k.X[i-15000:i], k.Y[i-15000:i], k.Z[i-15000:i])
            else:
                line.set_data_3d(k.X[:i], k.Y[:i], k.Z[:i])
            pt.set_data_3d(k.X[i], k.Y[i], k.Z[i])
        ax.view_init(0.005 * i, 0.05 * i)
        fig.canvas.draw()
        return lines + points

    anim = animation.FuncAnimation(fig, animate, init_func=init,
                                frames=18000//4, interval=5, blit=False)
                                
    # mywriter = animation.FFMpegWriter(bitrate=5000)
    # anim.save('test2.mp4', writer='fclearfmpeg', fps=20, extra_args=['-vcodec', 'libx264'])

    plt.show()