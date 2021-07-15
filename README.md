<div align="center">
<p>
    <img width="400" src="./docs/logoblack.svg">
</p>
<h1>Attractors - Python package</h1>

[![PyPI license](https://img.shields.io/github/workflow/status/Vignesh-Desmond/attractors/Build?style=flat-square&logo=GitHub)](https://github.com/Vignesh-Desmond/attractors/actions/workflows/build.yml)
[![PyPI version](https://img.shields.io/pypi/v/attractors?color=blue&style=flat-square)](https://pypi.python.org/pypi/attractors/)
[![PyPI license](https://img.shields.io/pypi/l/attractors?style=flat-square&color=orange)](https://lbesson.mit-license.org/)

Attractors is a package for simulation and visualization of strange attractors.

</div>

## Installation

The simplest way to install the module is via PyPi using pip

`pip install attractors`

Alternatively, the package can be installed via github as follows

```shell
git clone https://github.com/Vignesh-Desmond/attractors
cd attractors
python -m pip install .
```

To set up the package for development and debugging, it is recommended to use [Poetry](https://python-poetry.org/). Just install with
`poetry install` and let Poetry manage the environment and dependencies.

### Prerequisites

To generate video output, the package uses [ffmpeg](https://ffmpeg.org/). Download and install from [here](https://ffmpeg.org/download.html) according to your os and distribution and set PATH accordingly. Note that this is only required for generating video output.

## Basic Usage

A simple code snippet using the attractors package

```python
from attractors.attractor import Attractor

obj = Attractor("lorenz")
obj.rk3(0, 100, 10000)          #rk3(starttime, endtime, simpoints)
```

In the above snippet, `obj` is an Attractor instance with X, Y, and Z attributes, each being a 1D list of length _simpoints (number of points used for the simulation)_.

The parameters of each attractor can be given as kwargs as follows:

```python
obj = Attractor("lorenz", sigma = 5, rho = 28.5, init_coord = [0.2,0.1,0.1])
```

When parameters are not given, the default parameters are loaded for each attractor. In the above example, since `beta` is not given, the default value of 2.66667 is loaded.

To obtain the 3D coordinates of an attractor, we need to solve (usually) 3 non-linear ODE, one for each dimension. The solution can be derived via approximation using the [Runge-Kutta](https://en.wikipedia.org/wiki/Runge%E2%80%93Kutta_methods) methods. Currently, this package consists of the following iterative explicit RK methods:

- Euler
- RK2 (Heun, Ralston, Improved Polygon)
- RK3
- RK4
- RK5

For 2nd order Runge-Kutta, the method can be specified via the positional argument `rk2_method`

```python
obj.rk3(0, 100, 10000, rk2_method="heun")  #methods = "heun", "ralston", "imp_poly"
```

A list of attractors and ODE solvers can be obtained via the static methods `list_attractors()` and `list_des()` respectively.

## Plotting and Animation

The attractors package also comes with plotting and animation functions using [Matplotlib](https://matplotlib.org/). There are 2 plotting types, **Multipoint** and **Gradient**.

### Plot

Multipoint plot can be used to visualize multiple attractor objects which can be used to demonstrate the chaotic nature based on perturbances in initial conditions and parameters

The following sample code shows the usage of `plot_multipoint()`

```python
from attractors.attractor import Attractor
import numpy as np

n = 3
a = "rossler"
simtime = 100
simpoints = simtime * 100

# Create a list of n attractor instances
objs = [Attractor(a) for _ in range(n)]

# Change the initial coordinates randomly for n-1 objects
for i in range(n):
    objs[i].coord = (
        np.array(objs[i].coord) + [np.random.normal(0, 0.01) for _ in range(3)]
        if i != 0
        else np.array(objs[i].coord)
    )

# Solve the ODE equations
for obj in objs:
    func = getattr(obj, "rk3")
    func(0, simtime, simpoints)

# Use plot_multipoint to plot all the objects
ax = Attractor.plot_multipoint(
    simpoints - 1,
    *objs,
    dpi=240,
    bgcolor="#FFFFFF",
    palette=["#616161", "#7a7a7a", "#2e2e2e", "#1c1c1c"],
    linekwargs={"linewidth": 0.5, "alpha": 0.7},
    pointkwargs={"markersize": 1}
)
```

<div align="center">
<p>
<h5>The output figure generated for the code snippet</h5>
    <img src="./docs/plot.png">   
</p>
</div>

`plot_multipoint()` is a class method that requires 2 arguments:

- _index_ : timestep of the attractor objects on plot
- _\*objs_ : attractor objects to plot

Additionally, it also takes in multiple kwargs that

- set the figure parameters: _width, height, dpi_
- set the axes limits: _xlim, ylim, zlim_
- set line and point parameters via _linekwargs, pointkwargs_ (pass to matplotlib kwargs)
- set color
  - by _theme_
  - by manually by specifying _bgcolor_ (single hexcode) and _palette_ (list of hexcodes). Overrides theme settings if given.

The figure parameters, axes limits and theme can also be set via `set_figure()`, `set_limits()` and `set_theme()` methods respectively

`plot_gradient()` is similar to `plot_multipoint()`, however it can only take one attractor instance as input. And it also takes an extra kwarg: _gradientaxis_ to specify the axis along which the gradient is applied. (X, Y or Z).

Both `plot_gradient()` and `plot_multipoint()` returns an Matplotlib.axes object which can be used to display or save the figure and also change axes parameters after plotting.

### Animate

The Animate functions `set_animate_multipoint()` and `set_animate_gradient()` are similar to their plot function counterparts. By default, the visualization output will be saved in an MPEG4 encoded video. An example for gradient animation is as follows

```python
from attractors.attractor import Attractor

obj = Attractor("dequan_li")
obj.rk3(0, 10, 10000)

Attractor.set_animate_gradient(obj,
    width=10,
    height=10,
    theme="nord").animate(outf="example.mp4")
```

The above code generates a video `example.mp4` in the directory that it was run from. `animate` is a class method acting on the Attractor class instance. It has no required argmunents and it takes the following kwargs

- _live_: boolean arg to show the animated plot in a window interactively or save as output video.
- _fps_: frames per second of animation
- _outf_: filename of output video if generated
- _show_: boolean arg to disable `plt.show()` and return the Matplotlib.FuncAnimation instance (only when _live_ is True)

Both `set_animate_gradient()` and `set_animate_multipoint()` have 2 addititonal parameters: _elevationrate_ and _azimuthrate_ which control the rate of change of eleveation and azimuth angle for the duration of the animation respectively.

<div align="center">
<p>
<h5>Output animation (converted to gif and sliced for README) </h5>
    <img src="./docs/animate.gif">   
</p>
</div>

## CLI

The attractors package also comes with its own command-line parser. Simply type `attractors -h` to display the help message. The parser wraps the Attractor class and currently only supports animation.

The simplest way to visualize an Lorenz attractor is

```shell
attractors -p 100000 -s 100 -t multipoint lorenz
```

Each attractor also has its own parameters to set. The settings for each attractor can be obtained by the help command: `attractors ATTRACTOR -h`

## License

This package is licensed under the MIT License
