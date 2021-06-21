#!/usr/bin/env python
# -*- coding: utf-8 -*-

from src.anim.gradient import generate_video
from src.anim.sim import animate_simulation

# generate_video(nframes=5000, custom=True)
attractor = "lorenz"

theme = None
width = 16
height = 9
dpi = 120
sim_time = 200
points = 30000
bgcolor = theme["bgcolor"] if theme is not None else "#252a34"
palette = theme["palette"] if theme is not None else "hsv"
n = 3
integrator = "RK5"
# ['#BF616A', '#D08770', '#EBCB8B', '#A3BE8C', '#B48EAD', '#88C0D0']
animate_simulation(attractor, width, height, dpi, bgcolor, palette, sim_time, points, n, integrator)