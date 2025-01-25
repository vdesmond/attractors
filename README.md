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

# Creator's note

In the realm where mathematics transcends into art, strange attractors emerge as mesmerizing patterns that dance on the edge of chaos. This package is an attempt to visualize that: bringing rigorous numerical computation and stunning visualization that brings these mathematical marvels to life.

Born from a fascination with dynamical systems, I made the package `attractors` to provide an elegant interface to explore, simulate, and visualize the haunting beauty of chaotic systems. From the iconic spirals of the Lorenz attractor to the ethereal forms of lesser-known systems, each visualization tells a story of order emerging from chaos.

Now in its completely reimagined second iteration, `attractors` is now powered by Numba-accelerated computations and a modular architecture that supports extension in creating more solvers, systems, themes and visualizers while keeping the dependencies lean and code clean, typed and tested. In short, its artistic soul is kept as is, while I ported it to modern software design: clean, fast, and endlessly adaptable.

# Core Features

- A curated collection of 20+ strange attractors including classics and rare gems
- High-performance numerical solving using Numba-accelerated Runge-Kutta solvers
- Stunning visualizations with various themes and color mappings
- Modular design that welcomes extensions and experimentation

# Setup

For end user, it is just a pip installation

```bash
pip install attractors
```

Note that attractors depends on numba, so the system must be able to compile it. If any issues arise, visit numba installation (link)

# Basic Usage

In **v2.x** of attractors, registries are introduced to facilitate easier creation and usage of existing as well as new, custom systems solvers and themes. The following simple script demonstrates that well:

```python
from attractors import SystemRegistry, SolverRegistry, integrate_system
from attractors.visualizers import StaticPlotter
from attractors.themes import ThemeManager

# Get a system and solver
lorenz = SystemRegistry.get("lorenz")
solver = SolverRegistry.get("rk4")

# Generate trajectory
trajectory, time = integrate_system(lorenz, solver, steps=10000, dt=0.01)

# Visualize
theme = ThemeManager.get("nord")
StaticPlotter(lorenz, theme).visualize(trajectory)
plt.show()
```

Check out some [examples](examples/) for more inspiration. The [banner.py](examples/banner.py) for example was the code used to generate the README banner!

For a deeper dive into the package's capabilities, explore the complete [documentation](https://attractors.readthedocs.io/).

# Changelog

View the project's evolution in [changelog](CHANGELOG.md).

# Contributing

Contributions in any form are always appreciated. To get started, please read the [contributing guidelines](CONTRIBUTING.md) to familiarize yourself with the code and best practices.

# License

In spirit of open source code - [MIT License](LICENSE)
