"""
attractors
"""

from __future__ import annotations

from importlib.metadata import version

__version__ = version(__name__)

from attractors.solvers import rk4
from attractors.systems import lorenz
