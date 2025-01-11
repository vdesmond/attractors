from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any

import numpy as np
from matplotlib import pyplot as plt

from attractors.systems.registry import System
from attractors.themes.theme import Theme
from attractors.type_defs import Vector


class BasePlotter(ABC):
    VALID_COLOR_OPTIONS = ("time", "x", "y", "z")

    def __init__(
        self,
        system: System,
        theme: Theme,
        num_segments: int = 50,
        color_by: str | Callable[[Vector], Vector] = "time",
        color_cycles: float = 1.0,
        fig_kwargs: dict[str, Any] | None = None,
    ) -> None:
        self._validate_inputs(num_segments, color_cycles, color_by)
        self.system = system
        self.theme = theme
        self.num_segments = num_segments
        self.color_cycles = color_cycles
        self.fig_kwargs = fig_kwargs or {}
        self.color_by = color_by

    def _validate_inputs(
        self, num_segments: int, color_cycles: float, color_by: str | Callable[[Vector], Vector]
    ) -> None:
        if num_segments <= 0:
            raise ValueError("num_segments must be positive")
        if color_cycles <= 0:
            raise ValueError("color_cycles must be positive")
        if isinstance(color_by, str) and color_by not in self.VALID_COLOR_OPTIONS:
            error_message = f"color_by must be one of {self.VALID_COLOR_OPTIONS} or a callable"
            raise ValueError(error_message)

    def _setup_plot(self) -> None:
        self.fig = plt.figure(facecolor=self.theme.background, **self.fig_kwargs)
        self.ax = self.fig.add_subplot(111, projection="3d")
        self.ax.set_facecolor(self.theme.background)
        self.ax.set_axis_off()

        for axis in ["x", "y", "z"]:
            if self.system.plot_lims:
                getattr(self.ax, f"set_{axis}lim")(*self.system.plot_lims[f"{axis}lim"])  # type: ignore[literal-required]

    def __validate_color_values(self, values: Vector, trajectory: Vector) -> Vector:
        if not isinstance(values, np.ndarray):
            raise ValueError("Color function must return numpy array")
        if values.shape != (len(trajectory),):
            msg = f"Color function must return array of shape ({len(trajectory)},)"
            raise ValueError(msg)
        if not np.issubdtype(values.dtype, np.number):
            raise ValueError("Color function must return numeric array")
        if np.any(np.isnan(values)) or np.any(np.isinf(values)):
            raise ValueError("Color function returned NaN or Inf values")
        return (
            np.interp(values, (values.min(), values.max()), (0, 1))
            if values.max() != values.min()
            else values
        )

    def _get_color_values(self, trajectory: Vector) -> Vector:
        try:
            if callable(self.color_by):
                values = self.__validate_color_values(self.color_by(trajectory), trajectory)
            elif self.color_by == "time":
                values = np.linspace(0, 1, len(trajectory))
            else:
                values = self.__validate_color_values(
                    trajectory[:, {"x": 0, "y": 1, "z": 2}[self.color_by]], trajectory
                )
            return (values * self.color_cycles) % 1.0
        except Exception as e:
            msg = f"Error in color function: {e!s}"
            raise ValueError(msg) from e

    @abstractmethod
    def visualize(self, trajectory: Vector, **kwargs: Any) -> "BasePlotter":
        pass
