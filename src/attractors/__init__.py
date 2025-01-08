from pathlib import Path

from attractors.solvers import euler, rk2, rk3, rk4, rk5, stormer_verlet
from attractors.solvers.core import integrate_system
from attractors.solvers.registry import SolverRegistry
from attractors.systems import (
    finance,
    lorenz,
    rabinovich_fabrikant,
    rossler,
    thomas,
    wang_sun,
    yu_wang,
)
from attractors.systems.registry import SystemRegistry
from attractors.themes.manager import ThemeManager

theme_path = Path(__file__).parent / "themes" / "viz_themes.json"
ThemeManager.load(theme_path)
__all__ = ["SolverRegistry", "SystemRegistry", "ThemeManager", "integrate_system"]
