#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#  Copyright (c) 2021. Vignesh M
#  This file video.py, part of the attractors package is licensed under the MIT license.
#  See LICENSE.md in the project root for license information.
# ------------------------------------------------------------------------------


"""Module that handles video generation by piping matplotlib figure canvas to ffmpeg

Note:
    This module does not explicitly check for ffmpeg installation and does not handle errors related to that.
"""

import subprocess
from itertools import repeat

import matplotlib.figure as mfig
from pathos.pools import SerialPool
from tqdm import tqdm


def drawer(frame: int, fig: mfig.Figure, ufunc: callable) -> bytes:
    """Update function for pathos pool map which returns an RGB byte string of the canvas for ffmpeg pipe

    Args:
        frame (int): index to set data and draw canvas
        fig (matplotlib.figure.Figure): matplotlib figure instance
        ufunc (callable): animation function from Attractors class

    Returns:
        bytes: canvas as RGB byte-string
    """
    # proc = os.getpid()
    # print('{} by process {}'.format(frame,proc))
    ufunc(frame)
    fig.canvas.draw()
    return fig.canvas.tostring_rgb()


def ffmpeg_video(
    fig: mfig.Figure, update_func: callable, points: int, fps: int, outf: str
):
    """Generates output video given a animation function via ffmpeg

    Args:
        fig (matplotlib.figure.Figure): matplotlib figure instance
        update_func (callable): animation function from Attractors class
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
