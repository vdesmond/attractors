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

# Core Features

- A curated collection of 20+ strange attractors including classics and rare gems
- High-performance numerical solving using Numba-accelerated Runge-Kutta solvers
- Stunning visualizations with various themes and color mappings
- Modular design that welcomes extensions and experimentation

Read the full creator's note [here](https://attractors.vdesmond.com/#creators-note)

> [!NOTE]
> The version 2.x of attractors is a complete rewrite and is not backward compatible with the previous versions. Especially the API has been completely revamped, and the CLI support has been removed (though it might be added back in the future). If you are looking for the older version, you can find it in the [v1-legacy branch](https://github.com/vdesmond/attractors/tree/v1-legacy) and its related [documentation](https://attractors.rtfd.io/)

# Setup

For end user, it is just a pip installation

```bash
pip install attractors
```

Note that attractors depends on numba, so the system must be able to compile it. If any issues arise, look at [numba installation docs](https://numba.readthedocs.io/en/stable/user/installing.html).

# Basic Usage

In **v2.x** of attractors, registries are introduced to facilitate easier creation and usage of existing as well as new, custom systems solvers and themes. The following simple script demonstrates that well:

```python
from attractors import SystemRegistry, SolverRegistry, integrate_system
import matplotlib.pyplot as plt
from attractors.visualizers import StaticPlotter
from attractors.themes import ThemeManager

# Get system and solver from registry
system = SystemRegistry.get("lorenz")  # Using default parameters
solver = SolverRegistry.get("rk4")     # 4th order Runge-Kutta

# Generate trajectory
trajectory, time = integrate_system(system, solver, steps=10000, dt=0.01)

# Create visualization
theme = ThemeManager.get("nord")  # Using Nord color theme
plotter = StaticPlotter(system, theme)
plotter.visualize(trajectory)
plt.show()
```

Check out some [examples](examples/) for more inspiration. The [banner.py](examples/banner.py) for example was the code used to generate the README banner!

For a deeper dive into the package's capabilities, explore the complete [documentation](https://attractors.vdesmond.com/).

# License

In spirit of open source code - [MIT License](LICENSE)
