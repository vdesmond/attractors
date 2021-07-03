Attractors
==========

Attractors is a package for simulation and visualization of strange
attractors.

|PyPI license| |PyPI version| |image1|

.. |PyPI license| image:: https://img.shields.io/github/workflow/status/Vignesh-Desmond/attractors/Build?style=flat-square&logo=GitHub
   :target: https://github.com/Vignesh-Desmond/attractors/actions/workflows/build.yml
.. |PyPI version| image:: https://img.shields.io/pypi/v/attractors?color=blue&style=flat-square
   :target: https://pypi.python.org/pypi/attractors/
.. |image1| image:: https://img.shields.io/pypi/l/attractors?style=flat-square&color=orange
   :target: https://lbesson.mit-license.org/

For complete documentation, see the repository docs at
https://github.com/Vignesh-Desmond/attractors

Installation
------------

The package is currently hosted on PyPi and can be installed with pip:

``pip install attractors``

Alternatively, the package can be installed locally after cloning by the
following command:

``python -m pip install .``

Note:

The package requires FFMPEG as a prerequisite for generating
visualization output. For installation, see
`here <https://ffmpeg.org/download.html>`__

Dependencies
------------

-  Python (3.8+)
-  NumPy (1.21.0+)
-  Matplotlib (3.4.2+)

Usage
-----

The package is intended to be used mainly via the command-line
interface. The simplest way to visualize an Lorenz attractor is given
below:

::

   attractors -p 100000 -s 100 -t multipoint lorenz

``-p`` : Number of points for the simulation

``-s`` : Simulation time

``-t`` : Type of visualization

There are two types of visualizations:

``multipoint`` visualization can simulate multiple initial coordinates,
useful to infer the chaotic nature of the attractors. Use ``--n`` to set
the number of initial points.

``gradient`` visualization uses gradient color for the 3D plot, given a
specific axis.

By default, the visualization output will be saved in an MPEG4 encoded
video. To show a live plot, use the ``--live`` flag (only supported for
multipoint).

The full list of possible settings can be obtained by the help command:
``attractors -h``

::

   usage: attractors [-v] [-h] -t {multipoint,gradient}
                     [--des {euler,rk2,rk3,rk4,rk5}] [--width WIDTH]
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
     --des {euler,rk2,rk3,rk4,rk5}
                           set the Differential Equation Solver. Default: rk4
     --width WIDTH         set width of the figure Default: 16
     --height HEIGHT       set height of the figure Default: 9
     --dpi DPI             set DPI of the figure Default: 120
     --theme THEME         choose theme (color palette) to be used
     --bgcolor BGCOLOR     Background color for figure in hex. Overrides theme
                           settings Default: #000000
     --cmap CMAP           Matplotlib cmap for palette. Overrides theme settings
                           Default: jet
     --fps FPS             Set FPS for animated video (or interactive plot)
                           Default: 60
     --n N                 Number of initial points for Multipoint animation
                           Default: 3
     --rk2 {heun,imp_poly,ralston}
                           Method for 2nd order Runge-Kutta if specified to used.
                           Default: heun
     --outf OUTF           Output video filename Default: output.mp4
     --live                Live plotting instead of generating video.

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

Each attractor also has its own parameters to set. The settings for each
attractor can be obtained by the help command:
``attractors ATTRACTOR -h``

The help message for Lorenz attractors will be as follows:

::

   usage: attractors lorenz [-h] [--sigma SIGMA] [--beta BETA] [--rho RHO]
                            [--initcoord INITCOORD] [--xlim XLIM] [--ylim YLIM]
                            [--zlim ZLIM]

   optional arguments:
     -h, --help            show this help message and exit

   Lorenz attractor parameters:
     --sigma SIGMA         Parameter for Lorenz attractor Default: 5
     --beta BETA           Parameter for Lorenz attractor Default: 2.66667
     --rho RHO             Parameter for Lorenz attractor Default: 28
     --initcoord INITCOORD
                           Initial coordinate for Lorenz attractor. Input format:
                           "x,y,z" Default: [0.1, 0.1, 0.1]
     --xlim XLIM           x axis limits for figure. Input format: "xmin,xmax"
                           Default: [-20, 20]
     --ylim YLIM           y axis limits for figure. Input format: "ymin,ymax"
                           Default: [-30, 30]
     --zlim ZLIM           z axis limits for figure. Input format: "zmin,zmax"
                           Default: [5, 45]

License
-------

This package is licensed under the MIT License
