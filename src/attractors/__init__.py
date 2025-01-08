"""
attractors
"""

from __future__ import annotations

from importlib.metadata import version

from attractors.solvers import rk4
from attractors.systems import lorenz
from attractors.themes.manager import ThemeManager

ThemeManager.load("viz_themes.json")

__version__ = version(__name__)
__all__ = ["ThemeManager", "__version__", "lorenz", "rk4"]
