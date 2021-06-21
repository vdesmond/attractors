#!/usr/bin/env python
# -*- coding: utf-8 -*-

from src.anim.gradient import generate_video
from src.anim.sim import animate_simulation

# generate_video(nframes=5000, custom=True)
attractor = "chen"

theme = None
width = 16
height = 9
dpi = 120
sim_time = 50
points = 6000
bgcolor = theme["bgcolor"] if theme is not None else "#252a34"
palette = theme["palette"] if theme is not None else "hsv"

# ['#BF616A', '#D08770', '#EBCB8B', '#A3BE8C', '#B48EAD', '#88C0D0']
animate_simulation(attractor, width, height, dpi, bgcolor, palette, sim_time, points)