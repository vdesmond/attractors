<div align="center">
  <img src="https://res.cloudinary.com/vdesmond/image/upload/c_thumb,w_800,g_face/attractors_y4tepz.gif">
  <h1>attractors</h1>
  <em>in chaos, emerges beauty</em>
  <p>
</p>
  <p>A package for simulation and visualization of strange attractors.</p>
  <p><a href="https://codecov.io/gh/vdesmond/attractors"><img src="https://codecov.io/gh/vdesmond/attractors/branch/v2/graph/badge.svg?token=91EPQN331H" alt="codecov"></a>
<a href="https://github.com/vdesmond/attractors/actions"><img src="https://github.com/vdesmond/attractors/workflows/CI/badge.svg" alt="Actions status"></a>
<img src="https://img.shields.io/readthedocs/attractors" alt="Read the Docs">
<img src="https://img.shields.io/pypi/v/attractors" alt="PyPI - Version">
<img src="https://img.shields.io/pypi/pyversions/attractors" alt="PyPI - Python Version"></p>
  <p><a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff"></a>
<a href="https://github.com/astral-sh/uv"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json" alt="uv"></a></p>
</div>

[TOC]

## Creator's note
In the realm where mathematics transcends into art, strange attractors emerge as mesmerizing patterns that dance on the edge of chaos. This package is an attempt to visualize that: bringing rigorous numerical computation and stunning visualization that brings these mathematical marvels to life.

Born from a fascination with dynamical systems, I made the package *attractors* to provide an elegant interface to explore, simulate, and visualize the haunting beauty of chaotic systems. From the iconic spirals of the Lorenz attractor to the ethereal forms of lesser-known systems, each visualization tells a story of order emerging from chaos.

Now in its completely reimagined second iteration, *attractors* is now powered by Numba-accelerated computations and a modular architecture that supports extension in creating more solvers, systems, themes and visualizers while keeping the dependencies lean and code clean, typed and tested. In short, its artistic soul is kept as is, while I ported it to modern software design: clean, fast, and endlessly adaptable.

I hope you enjoy this package as much as I enjoyed creating it!

!!! warning
    The version 2.x of attractors is a complete rewrite and is not backward compatible with the previous versions. Especially the API has been completely revamped, and the CLI support has been removed (though it might be added back in the future). If you are looking for the older version, you can find it in the [v1.x branch](https://github.com/vdesmond/attractors/tree/v1-legacy)



## Core Features
- A curated collection of 20+ strange attractors including classics and rare gems
- High-performance numerical solving using Numba-accelerated Runge-Kutta solvers
- Stunning visualizations with various themes and color mappings
- Modular design that welcomes extensions and experimentation

Check out the [quickstart](quickstart.md) guide to get started with *attractors*!
