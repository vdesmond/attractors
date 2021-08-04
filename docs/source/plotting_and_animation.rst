Plotting and Animation
======================

The attractors package also comes with plotting and animation functions
using `Matplotlib <https://matplotlib.org/>`__. There are 2 plotting
types, **Multipoint** and **Gradient**.

Plot
----

Multipoint plot can be used to visualize multiple attractor objects
which can be used to demonstrate the chaotic nature based on
perturbances in initial conditions and parameters

The following sample code shows the usage of :meth:`.plot_multipoint()`

.. code:: python

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

:meth:`.plot_multipoint()` is a class method that requires 2 arguments:

-  *index* : timestep of the attractor objects on plot
-  *\*objs* : generator list

Additionally, it also takes in multiple kwargs that

-  set the figure parameters: *width, height, dpi*
-  set the axes limits: *xlim, ylim, zlim*
-  set line and point parameters via *linekwargs, pointkwargs* (pass to
   matplotlib kwargs)
-  set color

   -  by *theme*
   -  by manually by specifying *bgcolor* (single hexcode) and *palette*
      (list of hexcodes). Overrides theme settings if given.

The figure parameters, axes limits and theme can also be set via
:meth:`.set_figure()`, :meth:`.set_limits()` and :meth:`.set_theme()` methods
respectively

:meth:`.plot_gradient()` is similar to :meth:`.plot_multipoint()`, however it can
only take one generator as input. And it also takes an extra kwarg:
*gradientaxis* to specify the axis along which the gradient is applied.
(X, Y or Z).

Both :meth:`.plot_gradient()` and :meth:`.plot_multipoint()` returns an
Matplotlib.axes object which can be used to display or save the figure
and also change axes parameters after plotting.

Animate
-------

The Animate functions :meth:`.set_animate_multipoint()` and
:meth:`.set_animate_gradient()` are similar to their plot function
counterparts. By default, the visualization output will be saved in an
MPEG4 encoded video. An example for gradient animation is as follows

.. code:: python

   from attractors import Attractor

   obj = Attractor("dequan_li").rk3(0, 10, 10000)

   Attractor.set_animate_gradient(obj,
       width=10,
       height=10,
       theme="nord").animate(outf="example.mp4")

The above code generates a video ``example.mp4`` in the directory that
it was run from. :meth:`.animate` is a class method acting on the
:class:`.Attractor` class instance. It has no required argmunents and it takes
the following kwargs

-  *live*: boolean arg to show the animated plot in a window
   interactively or save as output video.
-  *fps*: frames per second of animation
-  *outf*: filename of output video if generated
-  *show*: boolean arg to disable ``plt.show()`` and return the
   Matplotlib.FuncAnimation instance (only when *live* is True)

Both :meth:`.set_animate_gradient()` and :meth:`.set_animate_multipoint()` have 2
additional parameters: *elevationrate* and *azimuthrate* which control
the rate of change of elevation and azimuth angle for the duration of
the animation respectively.
