Changelog
=========

`v1.3.0 <https://github.com/Vignesh-Desmond/attractors/releases/tag/1.3.0>`__
=============================================================================
:Date: 20 July, 2021

Announcements
-------------

*  Minor release with breaking changes (not backwards compatible)

Changes
-------

*  DES methods now return a generator instead of an ``Attractor``
   instance
-  X, Y, Z attributes of the ``Attractor`` are now single*valued floats
   instead of lists
*  Modified plotting and animation methods to support generators
*  Removed slice method
*  (Dev) Coverage tests

`commit history <https://github.com/Vignesh-Desmond/attractors/compare/1.2.0...1.3.0>`__

`v1.2.0 <https://github.com/Vignesh-Desmond/attractors/releases/tag/1.2.0>`__
=============================================================================
:Date: 15 July, 2021

.. _announcements-1:

Announcements
-------------

*  Minor version bump adding 2 new attractors

.. _changes-1:

Changes
-------

*  Added 2 new attractors : Dequan Li and Yu Wang
*  Removed legacy animate functions ``animate_gradient()`` and
   ``animate_sim()``
*  Added kwargs to control gradient axis, elevation and azimuth rate.
*  Added line and point kwargs to pass to matplotlib
*  Tweaked default params for multiple attractors
*  Minor bugfixes

`commit history <https://github.com/Vignesh-Desmond/attractors/compare/1.1.1...1.2.0>`__

`v1.1.1 <https://github.com/Vignesh-Desmond/attractors/releases/tag/1.1.1>`__
=============================================================================
:Date: 09 July, 2021

.. _announcements-2:

Announcements
-------------

*  Patch 1.1.1 for parser rewrite

.. _changes-2:

Changes
-------

*  parser rewrite based on Attractor class
*  parametrized testing (pytest)

`commit history <https://github.com/Vignesh-Desmond/attractors/compare/1.1.0...1.1.1>`__

`v1.1.0 <https://github.com/Vignesh-Desmond/attractors/releases/tag/1.1.0>`__
=============================================================================
:Date: 07 July, 2021

.. _announcements-3:

Announcements
-------------

*  Update of attractors package with various new features and bugfixes

.. _changes-3:

Changes
-------

*  Completely overhauled attractor class for modularity
*  Pooling update_func() for figure with pathos
*  New methods for setting various params independently
*  Included plotting methods
*  Bugfixes and minor QoL changes

`commit history <https://github.com/Vignesh-Desmond/attractors/compare/1.0.0...1.1.0>`__

`v1.0.0 <https://github.com/Vignesh-Desmond/attractors/releases/tag/1.0.0>`__
=============================================================================
:Date: 03 July, 2021

.. _announcements-4:

Announcements
-------------

*  First major release of attractors package

.. _changes-4:

Changes
-------

*  Rewrite of animate functions
*  New attractor module
*  Live gradient plotting

`commit history <https://github.com/Vignesh-Desmond/attractors/tree/1.0.0>`__
