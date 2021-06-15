#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import subprocess
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Line3DCollection
from runge_kutta import RK

def generate_video(nframes, custom=False, step=1):

    fig = plt.figure(figsize=(16, 9), dpi=120)
    canvas_width, canvas_height = fig.canvas.get_width_height()
    ax = fig.add_axes([0, 0, 1, 1], projection='3d')

    fig.set_facecolor('#2E3440') #! add bg argument
    ax.set_facecolor('#2E3440')   

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

    X = np.random.random(nframes)
    Y = np.random.random(nframes)
    Z = np.random.random(nframes)


    if not custom:
        cmap = plt.cm.get_cmap("hsv") #! add cmap argument
    else:
        from colortable import get_continuous_cmap
        cmap = get_continuous_cmap()

    line = Line3DCollection([], cmap=cmap) #! add hex argument
    ax.add_collection3d(line)

    def init():
        line.set_segments([])
        return line,

    init()
   
    def update(frame):

        #! gets slower over time :/
        
        steps = step
        i = (steps * frame) % len(X)
        points = np.array([X[:i], Y[:i], Z[:i]]).transpose().reshape(-1,1,3)
        segs = np.concatenate([points[:-1],points[1:]],axis=1)
        line.set_segments(segs)
        line.set_array(np.array(Y)) # set X, Y, Z for gradient
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

generate_video(nframes=6000, custom=True)