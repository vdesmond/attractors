attractors
==========

|Build status| |PyPI version| |PyPI license|

attractors is a package for simulation and visualization of strange
attractors.

Installation
============

The simplest way to install the module is via PyPi using pip

``pip install attractors``

Alternatively, the package can be installed via github as follows

::

   git clone https://github.com/Vignesh-Desmond/attractors
   cd attractors
   python -m pip install .

To set up the package for development and debugging, it is recommended
to use `Poetry <https://python-poetry.org/>`__. Just install with
``poetry install`` and let Poetry manage the environment and
dependencies.

Prerequisites
-------------

To generate video output, the package uses
`ffmpeg <https://ffmpeg.org/>`__. Download and install from
`here <https://ffmpeg.org/download.html>`__ according to your os and
distribution and set PATH accordingly. Note that this is only required
for generating video output.

Usage
=====

See
`documentation <https://github.com/Vignesh-Desmond/attractors/blob/main/README.md>`__
on github

Changelog
=========

See
`changelog <https://github.com/Vignesh-Desmond/attractors/blob/main/CHANGELOG.md>`__
for previous versions

License
=======

This package is licensed under the `MIT
License <https://github.com/Vignesh-Desmond/attractors/blob/main/LICENSE.md>`__

.. |Build status| image:: https://img.shields.io/github/workflow/status/Vignesh-Desmond/attractors/Build?style=flat-square&logo=GitHub
   :target: https://github.com/Vignesh-Desmond/attractors/actions/workflows/build.yml
.. |PyPI version| image:: https://img.shields.io/pypi/v/attractors?color=blue&style=flat-square
   :target: https://pypi.python.org/pypi/attractors/
.. |PyPI license| image:: https://img.shields.io/pypi/l/attractors?style=flat-square&color=orange
   :target: https://lbesson.mit-license.org/
