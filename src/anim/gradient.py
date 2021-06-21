#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os import initgroups
import numpy as np
import subprocess
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Line3DCollection
from src.utils.runge_kutta import RK
from src.utils.attractors import ATTRACTOR_PARAMS
from src.utils.colortable import get_continuous_cmap

def generate_video(attractor, width, height, dpi, bgcolor, palette, sim_time, points):

    fig = plt.figure(figsize=(width, height), dpi=dpi)

    canvas_width, canvas_height = fig.canvas.get_width_height()
    ax = fig.add_axes([0, 0, 1, 1], projection='3d')

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
    vect.RK5(0, sim_time, points) # ! integerator

    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_zlim(zlim)

    if isinstance(palette, str):
        cmap = plt.cm.get_cmap(palette)
    else:
        cmap = get_continuous_cmap(palette)

    line = Line3DCollection([], cmap=cmap)
    ax.add_collection3d(line)

    def init():
        line.set_segments([])
        return line,

    init()
   
    def update(frame):

        #! gets slower over time :/
        
        steps = step
        i = (steps * frame) % len(vect.X)
        points = np.array([vect.X[:i], vect.Y[:i], vect.Z[:i]]).transpose().reshape(-1,1,3)
        segs = np.concatenate([points[:-1],points[1:]],axis=1)
        line.set_segments(segs)
        line.set_array(np.array(vect.Y)) # set X, Y, Z for gradient
        ax.elev += 0.0001
        ax.azim += 0.1

    # Open an ffmpeg process
    outf = 'test.mp4'
    cmdstring = ('ffmpeg', 
                 '-y', '-r', '60', # overwrite, 1fps
                 '-s', '%dx%d' % (canvas_width, canvas_height),# size of image string
                 '-pix_fmt', 'argb', # format
                 '-f', 'rawvideo',  '-i', '-', # tell ffmpeg to expect raw video from the pipe
                  '-b:v', '5000k','-vcodec', 'mpeg4', outf) # output encoding
    p = subprocess.Popen(cmdstring, stdin=subprocess.PIPE)

    for frame in range(points):
        update(frame)
        fig.canvas.draw()
        string = fig.canvas.tostring_argb()
        p.stdin.write(string)

    p.communicate()