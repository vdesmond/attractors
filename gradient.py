#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pylab as plt
import subprocess
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Line3DCollection
from runge_kutta import RK

def generate_video(nframes):

    plt.style.use('dark_background')
    fig = plt.figure(figsize=(16, 9), dpi=120)
    canvas_width, canvas_height = fig.canvas.get_width_height()
    ax = fig.add_axes([0, 0, 1, 1], projection='3d')

    ax.w_xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.w_yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.w_zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))

    # Get rid of the spines
    ax.w_xaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
    ax.w_yaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
    ax.w_zaxis.line.set_color((1.0, 1.0, 1.0, 0.0))

    # Get rid of the ticks
    ax.set_xticks([]) 
    ax.set_yticks([]) 
    ax.set_zticks([])

    # * Bouali Type I
    r = [0, -2, -0.25]
    vect = RK(r, 'bouali_type_1', k=0.02, mu=0.4, b=0.2, p=10, q=0.1, s=50)
    vect.RK4(0, 200, nframes)

    ax.set_xlim((-0.05, 0.05))
    ax.set_ylim((-5, 5))
    ax.set_zlim((-0.2, 0.2))

    cmap = plt.cm.get_cmap("hsv")

    line = Line3DCollection([], cmap=cmap)
    ax.add_collection3d(line)

    line.set_segments([])

    def update(frame):
        steps = 1
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

    for frame in range(nframes):
        update(frame)
        fig.canvas.draw()
        string = fig.canvas.tostring_argb()
        p.stdin.write(string)

    p.communicate()

generate_video(nframes=5000)