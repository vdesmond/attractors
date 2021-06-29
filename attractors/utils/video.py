#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess


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
        "argb",  # format
        "-f",
        "rawvideo",
        "-i",
        "-",
        "-b:v",
        "5000k",
        "-vcodec",
        "mpeg4",
        outf,
    )
    p = subprocess.Popen(cmdstring, stdin=subprocess.PIPE)

    for frame in range(points):
        update_func(frame)
        fig.canvas.draw()
        string = fig.canvas.tostring_argb()
        p.stdin.write(string)

    p.communicate()
