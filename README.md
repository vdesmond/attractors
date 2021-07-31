<div align="center">
<p>
    <img width="400" src="./assets/logoblack.svg">
</p>
<h1>attractors</h1>

[![Build status](https://img.shields.io/github/workflow/status/Vignesh-Desmond/attractors/Build?style=flat-square&logo=GitHub)](https://github.com/Vignesh-Desmond/attractors/actions/workflows/build.yml)
[![PyPI version](https://img.shields.io/pypi/v/attractors?color=informational&style=flat-square)](https://pypi.python.org/pypi/attractors/)
[![PyPI license](https://img.shields.io/pypi/l/attractors?style=flat-square&color=orange)](https://lbesson.mit-license.org/)
[![PyPI Downloads](https://img.shields.io/pypi/dm/attractors?color=informational&style=flat-square)](https://pypi.python.org/pypi/attractors/)
[![codecov](https://codecov.io/gh/Vignesh-Desmond/attractors/branch/main/graph/badge.svg?token=2VKMZ5EYVS&style=flat-square)](https://codecov.io/gh/Vignesh-Desmond/attractors)

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
from attractors import Attractor

obj = Attractor("lorenz").rk3(0, 100, 10000) #rk3(starttime, endtime, simpoints)
```

In the above snippet, `obj` is an generator instance yielding an attractor instance with X, Y, and Z attributes. The generator reaches `StopIteration` after iterating _simpoints (number of points used for the simulation)_ times.

The parameters of each attractor can be given as kwargs as follows:

```python
attr = Attractor("lorenz", sigma = 5, rho = 28.5, init_coord = [0.2,0.1,0.1])
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
obj = attr.rk3(0, 100, 10000, rk2_method="heun")  #methods = "heun", "ralston", "imp_poly"
```

A list of attractors and ODE solvers can be obtained via the static methods `list_attractors()` and `list_des()` respectively.

## Plotting and Animation

The attractors package also comes with plotting and animation functions using [Matplotlib](https://matplotlib.org/). There are 2 plotting types, **Multipoint** and **Gradient**.

### Plot

Multipoint plot can be used to visualize multiple attractor objects which can be used to demonstrate the chaotic nature based on perturbances in initial conditions and parameters

The following sample code shows the usage of `plot_multipoint()`

```python
from attractors import Attractor
import numpy as np

n = 3
a = "rossler"
simtime = 100
simpoints = simtime * 100

# Create a list of n attractor instances
attrs = [Attractor(a) for _ in range(n)]

# Change the initial coordinates randomly for n-1 objects
for attr in attrs[1:]:
    attr.coord += np.random.normal(0, 0.01, size=3)

# Solve the ODE equations and store the generators
objs = []
for a in attrs:
    func = getattr(a, "rk3")
    objs.append(func(0, simtime, simpoints))

# Use plot_multipoint with necessary kwargs
ax = Attractor.plot_multipoint(
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
    <img src="./assets/plot.png">   
</p>
</div>

`plot_multipoint()` is a class method that requires only one argument:

- _\*objs_ : generator list

Additionally, it also takes in multiple kwargs that

- set the figure parameters: _width, height, dpi_
- set the axes limits: _xlim, ylim, zlim_
- set line and point parameters via _linekwargs, pointkwargs_ (pass to matplotlib kwargs)
- set color
  - by _theme_
  - by manually by specifying _bgcolor_ (single hexcode) and _palette_ (list of hexcodes). Overrides theme settings if given.
  - plot at a specific time ts: _index_

The figure parameters, axes limits and theme can also be set via `set_figure()`, `set_limits()` and `set_theme()` methods respectively

`plot_gradient()` is similar to `plot_multipoint()`, however it can only take one generator as input. And it also takes an extra kwarg: _gradientaxis_ to specify the axis along which the gradient is applied. (X, Y or Z).

Both `plot_gradient()` and `plot_multipoint()` returns an Matplotlib.axes object which can be used to display or save the figure and also change axes parameters after plotting.

### Animate

The Animate functions `set_animate_multipoint()` and `set_animate_gradient()` are similar to their plot function counterparts. By default, the visualization output will be saved in an MPEG4 encoded video. An example for gradient animation is as follows

```python
from attractors import Attractor

obj = Attractor("dequan_li").rk3(0, 10, 10000)

Attractor.set_animate_gradient(obj,
    width=10,
    height=10,
    theme="nord").animate(outf="example.mp4")
```

The above code generates a video `example.mp4` in the directory that it was run from. `animate` is a class method acting on the `Attractor` class instance. It has no required argmunents and it takes the following kwargs

- _live_: boolean arg to show the animated plot in a window interactively or save as output video.
- _fps_: frames per second of animation
- _outf_: filename of output video if generated
- _show_: boolean arg to disable `plt.show()` and return the Matplotlib.FuncAnimation instance (only when _live_ is True)

Both `set_animate_gradient()` and `set_animate_multipoint()` have 2 addititonal parameters: _elevationrate_ and _azimuthrate_ which control the rate of change of eleveation and azimuth angle for the duration of the animation respectively.

<div align="center">
<p>
<h5>Output animation (converted to gif and sliced for README) </h5>
    <img src="./assets/animate.gif">   
</p>
</div>

## CLI

The attractors package also comes with its own command-line parser as a legacy interface (from v1.0.0). Simply type `attractors -h` to display the help message. The parser wraps the Attractor class and **only supports animation**.

The simplest way to visualize an Lorenz attractor is

```shell
attractors -p 100000 -s 100 -t multipoint lorenz
```

#### Full help:

```console
$ attractors -h
usage: attractors [-v] [-h] -t {multipoint,gradient}
                  [--des {rk2,rk3,euler,rk5,rk4}] [--width WIDTH]
                  [--height HEIGHT] [--dpi DPI] [--theme THEME] -s SIMTIME -p
                  SIMPOINTS [--bgcolor BGCOLOR] [--cmap CMAP] [--fps FPS]
                  [--n N] [--rk2 {heun,imp_poly,ralston}] [--outf OUTF]
                  [--live]
                  ATTRACTOR ...

optional arguments:
  -v, --version         show program's version number and exit
  -h, --help            show this help message and exit

required arguments:
  -t {multipoint,gradient}, --type {multipoint,gradient}
                        choose simulation type
  -s SIMTIME, --simtime SIMTIME
                        set the simulation time
  -p SIMPOINTS, --simpoints SIMPOINTS
                        set the number of points to be used for the simulation

other arguments:
  --des {rk2,rk3,euler,rk5,rk4}
                        choose the Differential Equation Solver. Default: rk4
  --width WIDTH         set width of the figure Default: 16
  --height HEIGHT       set height of the figure Default: 9
  --dpi DPI             set DPI of the figure Default: 120
  --theme THEME         choose theme (color palette) to be used
  --bgcolor BGCOLOR     background color for figure in hex. Overrides theme
                        settings if specified Default: #000000
  --cmap CMAP           matplotlib cmap for palette. Overrides theme settings
                        if specified Default: jet
  --fps FPS             set FPS for animated video (or interactive plot)
                        Default: 60
  --n N                 number of initial points for Multipoint animation
                        Default: 3
  --rk2 {heun,imp_poly,ralston}
                        method for 2nd order Runge-Kutta if specified to be
                        used. Default: heun
  --outf OUTF           output video filename Default: output.mp4
  --live                live plotting instead of generating video.

Attractor settings:
  Choose one of the attractors and specify its parameters

  ATTRACTOR
    lorenz              Lorenz attractor
    rabinovich_fabrikant
                        Rabinovich Fabrikant attractor
    lotka_volterra      Lotka Volterra attractor
    rossler             Rossler attractor
    wang_sun            Wang Sun attractor
    rikitake            Rikitake attractor
    nose_hoover         Nose Hoover attractor
    aizawa              Aizawa attractor
    three_cell_cnn      Three Cell CNN attractor
    bouali_type_1       Bouali Type 1 attractor
    bouali_type_2       Bouali Type 2 attractor
    bouali_type_3       Bouali Type 3 attractor
    finance             Finance attractor
    burke_shaw          Burke Shaw attractor
    moore_spiegel       Moore Spiegel attractor
    sakarya             Sakarya attractor
    dadras              Dadras attractor
    halvorsen           Halvorsen attractor
    hadley              Hadley attractor
    chen                Chen attractor
    chen_lee            Chen Lee attractor
    chen_celikovsky     Chen Celikovsky attractor
    thomas_cyclically_symmetric
                        Thomas Cyclically Symmetric attractor
    dequan_li           Dequan Li attractor
    yu_wang             Yu Wang attractor

```

Each attractor also has its own parameters to set. The settings for each attractor can be obtained by the help command: `attractors ATTRACTOR -h`

#### Attractor help

```console
$ attractors finance -h
usage: attractors finance [-h] [--a A] [--b B] [--c C]
                          [--initcoord INITCOORD INITCOORD INITCOORD]
                          [--xlim XLIM XLIM] [--ylim YLIM YLIM]
                          [--zlim ZLIM ZLIM]

optional arguments:
  -h, --help            show this help message and exit

Finance attractor parameters:
  --a A                 Parameter for Finance attractor Default: 1e-05
  --b B                 Parameter for Finance attractor Default: 0.1
  --c C                 Parameter for Finance attractor Default: 1.0
  --initcoord INITCOORD INITCOORD INITCOORD
                        Initial coordinate for Finance attractor. Input
                        format: "x y z" Default: [0.0, -10.0, 0.1]
  --xlim XLIM XLIM      x axis limits for figure. Input format: "xmin xmax"
                        Default: [-3.0, 3.0]
  --ylim YLIM YLIM      y axis limits for figure. Input format: "ymin ymax"
                        Default: [-5.0, -15.0]
  --zlim ZLIM ZLIM      z axis limits for figure. Input format: "zmin zmax"
                        Default: [-1.5, 1.5]
```

## Changelog

See [changelog](https://github.com/Vignesh-Desmond/attractors/blob/main/CHANGELOG.md) for previous versions

## Development

This package is under early stages of development it's open to any constructive suggestions. Please send bug reports and feature requests through issue trackers and pull requests.

## License

This package is licensed under the [MIT License](https://github.com/Vignesh-Desmond/attractors/blob/main/LICENSE)
