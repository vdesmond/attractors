#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import subprocess
from itertools import repeat

from pathos.pools import ParallelPool, ProcessPool, SerialPool, ThreadPool
from tqdm import tqdm


def drawer(frame, fig, ufunc):
    # proc = os.getpid()
    # print('{} by process {}'.format(frame,proc))
    ufunc(frame)
    fig.canvas.draw()
    canvas_string = fig.canvas.tostring_argb()
    return canvas_string


def ffmpeg_video(fig, update_func, points, fps, outf):
    """Generates output video given a animation function via ffmpeg

    Args:
        fig (matplotlib.figure.Figure): matplotlib figure instance
        update_func (callable): animation function
        points (int): number of points used for the simulation
        fps (int): frames per second for output video
        outf (str): output video filename
    """
    outf = "pathos.mp4"
    canvas_width, canvas_height = fig.canvas.get_width_height()
    cmdstring = (
        "ffmpeg",
        "-y",
        "-r",
        "%d" % fps,
        "-s",
        "%dx%d" % (canvas_width, canvas_height),
        "-pix_fmt",
        "argb",  # format
        "-f",
        "rawvideo",
        "-i",
        "-",
        "-b:v",
        "5000k",
        "-vcodec",
        "mpeg4",
        "-threads",
        "12",
        "-loglevel",
        "quiet",
        outf,
    )

    import time

    x = time.time()

    pool = SerialPool()
    results = pool.imap(drawer, range(0, points), repeat(fig), repeat(update_func))

    p = subprocess.Popen(cmdstring, stdin=subprocess.PIPE)

    for frame in tqdm(results, total=points):
        p.stdin.write(frame)

    p.communicate()
    pool.close()
    pool.terminate()

    print(time.time() - x)
