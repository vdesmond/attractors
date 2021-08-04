Basic Usage
===========

A simple code snippet using the attractors package

.. code:: python

   from attractors import Attractor

   obj = Attractor("lorenz").rk3(0, 100, 10000) #rk3(starttime, endtime, simpoints)

In the above snippet, ``obj`` is an generator instance yielding an
attractor instance with X, Y, and Z attributes. The generator reaches
``StopIteration`` after iterating *simpoints (number of points used for
the simulation)* times.

The parameters of each attractor can be given as kwargs as follows:

.. code:: python

   attr = Attractor("lorenz", sigma = 5, rho = 28.5, init_coord = [0.2,0.1,0.1])

When parameters are not given, the default parameters are loaded for
each attractor. In the above example, since ``beta`` is not given, the
default value of 2.66667 is loaded.

To obtain the 3D coordinates of an attractor, we need to solve (usually)
3 non-linear ODE, one for each dimension. The solution can be derived
via approximation using the
`Runge-Kutta <https://en.wikipedia.org/wiki/Runge%E2%80%93Kutta_methods>`__
methods. Currently, this package consists of the following iterative
explicit RK methods:

-  Euler
-  RK2 (Heun, Ralston, Improved Polygon)
-  RK3
-  RK4
-  RK5

For 2nd order Runge-Kutta, the method can be specified via the
positional argument ``rk2_method``

.. code:: python

   obj = attr.rk3(0, 100, 10000, rk2_method="heun")
    #methods = "heun", "ralston", "imp_poly"

A list of attractors and ODE solvers can be obtained via the static
methods ``list_attractors()`` and ``list_des()`` respectively.
