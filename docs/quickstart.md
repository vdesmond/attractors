# Getting Started

## Installation

The simplest way to install `attractors` is via pip:

```bash
pip install attractors
```

For users who prefer modern Python packaging tools, you can also install using [uv](https://github.com/astral-sh/uv):

```bash
uv install attractors
```

### System Requirements

- Python 3.11 or higher
- Primarily the package uses 3 main dependencies:
  - `numpy` for numerical computation
  - `numba` for accelerated computation
  - `matplotlib` for visualization

!!! note

    A system must be able to compile `numba` for the package to work. If any issues arise, look at the [numba installation docs](https://numba.readthedocs.io/en/stable/user/installing.html).

## Quick Start

Here's a minimal example to visualize the Rossler attractor:

```python
--8<-- "examples/quick_start.py"
```

This script will generate a visualization of the Rossler attractor using the default parameters. Once run, you should see a plot of the attractor saved in an image file as follows:

[![Rossler attractor](https://res.cloudinary.com/vdesmond/image/upload/v1737877526/output_ncppaa.png)](https://res.cloudinary.com/vdesmond/image/upload/v1737877526/output_ncppaa.png)
/// caption
Rossler attractor
///

voila! You've just created your first attractor visualization! But what did we just do? For that, I recommend you to start with the [user guide](guides/overview.md) to understand the underlying concepts, and design principles of the package, and from there, you can not only create custom visualizations of the various systems we have with the existing solvers and themes but also create your own systems, solvers, and themes to extend the package!
