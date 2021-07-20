#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import subprocess
from itertools import repeat

from pathos.pools import SerialPool
from tqdm import tqdm


def drawer(frame, fig, ufunc):
    """Update function for pathos pool map
    which returns an ARBG byte string of the canvas
    for ffmpeg pipe

    Args:
        frame (int): index to set data and draw canvas
        fig (matplotlib.figure.Figure): matplotlib figure instance
        ufunc (callable): animation function

    Returns:
        bytes: canvas as ARGB byte-string
    """
    # proc = os.getpid()
    # print('{} by process {}'.format(frame,proc))
    ufunc(frame)
    fig.canvas.draw()
    return fig.canvas.tostring_rgb()


def ffmpeg_video(fig, update_func, points, fps, outf):
    """Generates output video given a animation function via ffmpeg

    Args:
        fig (matplotlib.figure.Figure): matplotlib figure instance
        update_func (callable): animation function
        points (int): number of points used for the simulation
        fps (int): frames per second for output video
        outf (str): output video filename
    """
    canvas_width, canvas_height = fig.canvas.get_width_height()
    cmdstring = (
        "ffmpeg",
        "-y",
        "-r",
        "%d" % fps,
        "-s",
        "%dx%d" % (canvas_width, canvas_height),
        "-pix_fmt",
        "rgb24",  # format
        "-f",
        "rawvideo",
        "-i",
        "-",
        "-b:v",
        "5000k",
        "-vcodec",
        "libx264",
        "-threads",
        "12",
        "-loglevel",
        "quiet",
        outf,
    )

    pool = SerialPool()
    results = pool.imap(drawer, range(points), repeat(fig), repeat(update_func))

    p = subprocess.Popen(cmdstring, stdin=subprocess.PIPE)

    for frame in tqdm(results, total=points):
        p.stdin.write(frame)
        p.stdin.flush()

    p.communicate()
    pool.close()
    pool.terminate()
