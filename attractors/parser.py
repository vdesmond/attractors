#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import json
from argparse import SUPPRESS

import numpy as np

from attractors.attractor import ATTRACTOR_PARAMS, Attractor

try:
    import importlib.metadata as metadata
    import importlib.resources as pkg_resources
except ImportError:
    import importlib_resources as pkg_resources
    import importlib_metadata as metadata

from attractors import data


def case_convert(snakecase_string):
    return snakecase_string.replace("_", " ").title().replace("Cnn", "CNN")


def cli():
    parser = argparse.ArgumentParser(add_help=False, argument_default=argparse.SUPPRESS)
    required = parser.add_argument_group("required arguments")
    optional = parser.add_argument_group("other arguments")

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=metadata.version("attractors"),
    )

    parser.add_argument(
        "-h",
        "--help",
        action="help",
        help="show this help message and exit",
    )

    required.add_argument(
        "-t",
        "--type",
        help="choose simulation type",
        type=str,
        choices=["multipoint", "gradient"],
        required=True,
    )

    optional.add_argument(
        "--des",
        help="choose the Differential Equation Solver. Default: rk4",
        type=str,
        choices=Attractor.list_des(),
        default="rk4",
    )

    optional.add_argument(
        "--width",
        help="set width of the figure Default: 16",
        type=int,
    )
    optional.add_argument(
        "--height",
        help="set height of the figure Default: 9",
        type=int,
    )
    optional.add_argument(
        "--dpi",
        help="set DPI of the figure Default: 120",
        type=int,
    )
    optional.add_argument(
        "--theme", help="choose theme (color palette) to be used", type=str
    )
    required.add_argument(
        "-s",
        "--simtime",
        help="set the simulation time",
        type=int,
        required=True,
    )
    required.add_argument(
        "-p",
        "--simpoints",
        help="set the number of points to be used for the simulation",
        type=int,
        required=True,
    )
    optional.add_argument(
        "--bgcolor",
        help=(
            "background color for figure in hex. Overrides theme settings if"
            " specified Default: #000000"
        ),
        type=str,
    )
    optional.add_argument(
        "--cmap",
        help=(
            "matplotlib cmap for palette. Overrides theme settings if"
            " specified Default: jet"
        ),
        type=str,
    )
    optional.add_argument(
        "--fps",
        help="set FPS for animated video (or interactive plot) Default: 60",
        type=int,
    )
    optional.add_argument(
        "--n",
        help="number of initial points for Multipoint animation Default: 3",
        type=int,
        default=3,
    )
    optional.add_argument(
        "--rk2",
        help=(
            "method for 2nd order Runge-Kutta if specified to be used." " Default: heun"
        ),
        type=str,
        choices=["heun", "imp_poly", "ralston"],
        default="heun",
    )
    optional.add_argument(
        "--outf",
        help="output video filename Default: output.mp4",
        type=str,
    )
    optional.add_argument(
        "--live",
        help="live plotting instead of generating video.",
        action="store_true",
    )
    subparsers = parser.add_subparsers(
        title="Attractor settings",
        description="Choose one of the attractors and specify its parameters",
        dest="attractor",
        metavar="ATTRACTOR",
    )

    for attr, attrparams in ATTRACTOR_PARAMS.items():
        attrparser = subparsers.add_parser(
            f"{attr}",
            help=f"{case_convert(attr)} attractor",
            argument_default=argparse.SUPPRESS,
        )
        attrgroup = attrparser.add_argument_group(
            title=f"{case_convert(attr)} attractor parameters"
        )

        for i in range(len(attrparams["params"])):
            attrgroup.add_argument(
                f"--{attrparams['params'][i]}",
                help=(
                    f"Parameter for {case_convert(attr)} attractor "
                    f"Default: {attrparams['default_params'][i]}"
                ),
                type=float,
            )
        attrgroup.add_argument(
            "--initcoord",
            help=(
                f"Initial coordinate for {case_convert(attr)} attractor. Input"
                f" format: \"x y z\" Default: {attrparams['init_coord']}"
            ),
            type=float,
            nargs=3,
        )
        for k in ["x", "y", "z"]:
            attrgroup.add_argument(
                f"--{k}lim",
                help=(
                    f"{k} axis limits for figure. Input format:"
                    f" \"{k}min {k}max\" Default: {attrparams[f'{k}lim']}"
                ),
                type=float,
                nargs=2,
            )

    args = parser.parse_args()
    kwargs = vars(args)

    attractor = args.attractor
    if args.type == "multipoint":
        objs = [Attractor(attractor, kwargs=kwargs) for _ in range(args.n)]
        for i in range(args.n):
            objs[i].coord = (
                np.array(objs[i].coord) + [np.random.normal(0, 0.01) for _ in range(3)]
                if i != 0
                else np.array(objs[i].coord)
            )
        itrs = []
        for obj in objs:
            func = getattr(obj, args.des)
            if args.des == "rk2":
                itr = func(0, args.simtime, args.simpoints, args.rk2)
            else:
                itr = func(0, args.simtime, args.simpoints)
            itrs.append(itr)
        Attractor.set_animate_multipoint(*itrs, **kwargs).animate(**kwargs)
    else:
        obj = Attractor(attractor, kwargs=kwargs)
        func = getattr(obj, args.des)
        if args.des == "rk2":
            itr = func(0, args.simtime, args.simpoints, args.rk2)
        else:
            itr = func(0, args.simtime, args.simpoints)
        Attractor.set_animate_gradient(itr, **kwargs).animate(**kwargs)


if __name__ == " __main__":
    cli()
