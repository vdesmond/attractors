#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import json
from src.anim.gradient import animate_gradient
from src.anim.sim import animate_simulation

with open('./src/data/themes.json') as f:
    themes = json.load(f)

attractor = "chen"
theme = themes["Builtin Solarized Light"]

palette_temp = list(theme.values())
palette_temp.remove(theme["background"])

width = 16
height = 9
dpi = 120
sim_time = 10
points = 5000
bgcolor = theme["background"] if theme is not None else "#000000"
palette = palette_temp if theme is not None else "jet"

n = 6
integrator = "RK5"

# animate_simulation(attractor, width, height, dpi, bgcolor, palette, sim_time, points, n, integrator)
animate_gradient(attractor, width, height, dpi, bgcolor, palette, sim_time, points, integrator)