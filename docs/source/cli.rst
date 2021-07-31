CLI
===

The attractors package also comes with its own command-line parser as a
legacy interface (from ``v1.0.0``). Simply type ``attractors -h`` to display
the help message. The parser wraps the Attractor class and **only
supports animation**.

The simplest way to visualize an Lorenz attractor is

.. code:: shell

   attractors -p 100000 -s 100 -t multipoint lorenz

`Full help message`

.. code:: console

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

Each attractor also has its own parameters to set. The settings for each
attractor can be obtained by the help command:
``attractors ATTRACTOR -h``

`Attractor help message`

.. code:: console

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
