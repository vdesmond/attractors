#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import json
from src.anim.gradient import animate_gradient
from src.anim.sim import animate_simulation
from argparse import SUPPRESS

parser = argparse.ArgumentParser(add_help=False)
required = parser.add_argument_group('required arguments')
optional = parser.add_argument_group('optional arguments')

# Add back help 
optional.add_argument(
    '-h',
    '--help',
    action='help',
    default=SUPPRESS,
    help='show this help message and exit'
)

# required.add_argument(
#     "attractor",
#     help=("Attractor to be simulated"),
#     type=str,
# )

optional.add_argument(
    "--width",
    help=("Width of the figure" " Default: 16"),
    type=int,
    default=16,
)
optional.add_argument(
    "--height",
    help=("Height of the figure" " Default: 9"),
    type=int,
    default=9,
)
optional.add_argument(
    "--dpi",
    help=("DPI of the figure" " Default: 120"),
    type=int,
    default=120,
)
optional.add_argument(
    "-t",
    "--theme",
    help=("Theme (color palette) to be used"),
    type=str
)
required.add_argument(
    "-s",
    "--simtime",
    help=("Simulation time"),
    type=int,
    required=True
)
required.add_argument(
    "-p",
    "--simpoints",
    help=("Number of points to be used for the simulation."),
    type=int,
    required=True
)
optional.add_argument(
    "--bgcolor",
    help=("Background color for figure in hex. Overrides theme settings."" Default: #000000"),
    type=str,
    default="#000000"
)
optional.add_argument(
    "--cmap",
    help=("Matplotlib cmap for palette. Overrides theme settings."" Default: jet"),
    type=str,
    default="jet"
)

subparsers = parser.add_subparsers(help='Simulation type')
parser_a = subparsers.add_parser('multipoint', help='Multipoint simulation')

parser_a.add_argument(
    "--n",
    help=("Number of initial points." " Default: 3"),
    type=int,
    default=3,
)

parser_b = subparsers.add_parser('gradient', help='Gradient simulation')
parser_b.add_argument(
    "--n",
    help=("Number of initial points." " Default: 3"),
    type=int,
    default=3,
)

args = parser.parse_args()
args1 = parser_a.parse_args()
print(vars(args))












with open("./src/data/themes.json") as f:
    themes = json.load(f)

attractor = "chen"
theme = themes["AtelierSulphurpool"]

palette_temp = list(theme.values())
palette_temp.remove(theme["background"])

width = 16
height = 9
dpi = 120
sim_time = 20
points = 5000
bgcolor = theme["background"] if theme is not None else "#000000"
palette = palette_temp if theme is not None else "jet"

n = 6
integrator = "RK5"

animate_simulation(
    attractor,
    width,
    height,
    dpi,
    bgcolor,
    palette,
    sim_time,
    points,
    n,
    integrator,
    interactive=False,

)
# animate_gradient(
#     attractor, width, height, dpi, bgcolor, palette, sim_time, points, integrator
# )
