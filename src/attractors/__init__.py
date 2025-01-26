from pathlib import Path

from attractors.solvers.core import integrate_system
from attractors.solvers.registry import Solver, SolverRegistry
from attractors.systems.registry import System, SystemRegistry
from attractors.themes.manager import ThemeManager
from attractors.themes.theme import Theme
from attractors.visualizers.animate import AnimatedPlotter, AnimatedVisualizeKwargs
from attractors.visualizers.base import BasePlotter
from attractors.visualizers.static import StaticPlotter
from attractors.visualizers.utils.color_mapper import ColorMapper
from attractors.visualizers.utils.downsampler import CompressionMethod

theme_path = Path(__file__).parent / "themes" / "viz_themes.json"
ThemeManager.load(theme_path)
__all__ = [
    "AnimatedPlotter",
    "AnimatedVisualizeKwargs",
    "BasePlotter",
    "ColorMapper",
    "CompressionMethod",
    "Solver",
    "SolverRegistry",
    "StaticPlotter",
    "System",
    "SystemRegistry",
    "Theme",
    "ThemeManager",
    "integrate_system",
]
