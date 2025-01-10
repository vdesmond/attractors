from pathlib import Path

from attractors.solvers.core import integrate_system
from attractors.solvers.registry import SolverRegistry
from attractors.systems.registry import SystemRegistry
from attractors.themes.manager import ThemeManager
from attractors.themes.theme import Theme
from attractors.visualizers.static import StaticPlotter

theme_path = Path(__file__).parent / "themes" / "viz_themes.json"
ThemeManager.load(theme_path)
__all__ = [
    "SolverRegistry",
    "StaticPlotter",
    "SystemRegistry",
    "Theme",
    "ThemeManager",
    "integrate_system",
]
