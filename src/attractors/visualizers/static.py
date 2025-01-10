from collections.abc import Callable
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray

from attractors.type_defs import Vector


class StaticPlotter:
    VALID_COLOR_OPTIONS = ("time", "x", "y", "z")

    def __init__(
        self,
        system: Any,
        theme: Any,
        num_segments: int = 50,
        color_by: str | Callable[[NDArray[np.float64]], NDArray[np.float64]] = "time",
        color_cycles: float = 1.0,
        fig_kwargs: dict[str, Any] | None = None,
        line_kwargs: dict[str, Any] | None = None,
    ) -> None:
        if num_segments <= 0:
            raise ValueError("num_segments must be positive")
        if color_cycles <= 0:
            raise ValueError("color_cycles must be positive")
        self.system = system
        self.theme = theme
        self.num_segments = num_segments
        self.color_cycles = color_cycles
        self.fig_kwargs = fig_kwargs or {}
        self.line_kwargs = line_kwargs or {}
        if isinstance(color_by, str) and color_by not in self.VALID_COLOR_OPTIONS:
            msg = f"color_by must be one of {self.VALID_COLOR_OPTIONS} or a callable"
            raise ValueError(msg)
        self.color_by = color_by

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

    def __get_color_values(self, trajectory: Vector) -> Vector:
        try:
            if callable(self.color_by):
                values = self.__validate_color_values(
                    self.color_by(trajectory), trajectory
                )
            elif self.color_by == "time":
                values = np.linspace(0, 1, len(trajectory))
            else:
                values = self.__validate_color_values(
                    trajectory[:, {"x": 0, "y": 1, "z": 2}[self.color_by]], trajectory
                )
            return (values * self.color_cycles) % 1.0
        except Exception as e:
            error_message = f"Error in color function: {e!s}"
            raise ValueError(error_message) from e

    def plot(self, trajectory: Vector) -> "StaticPlotter":
        self.fig = plt.figure(facecolor=self.theme.background, **self.fig_kwargs)
        self.ax = self.fig.add_subplot(111, projection="3d")
        self.ax.set_facecolor(self.theme.background)
        self.ax.set_axis_off()

        segment_length = len(trajectory) // self.num_segments
        color_values = self.__get_color_values(trajectory)

        for i in range(self.num_segments):
            start_idx = i * segment_length
            end_idx = start_idx + segment_length
            self.ax.plot(
                trajectory[start_idx:end_idx, 0],
                trajectory[start_idx:end_idx, 1],
                trajectory[start_idx:end_idx, 2],
                "-",
                c=self.theme.colormap(color_values[start_idx:end_idx].mean()),
                **self.line_kwargs,
            )

        axis_limits = {
            axis: getattr(self.ax, f"set_{axis}lim") for axis in ["x", "y", "z"]
        }
        for axis, set_lim in axis_limits.items():
            set_lim(*self.system.plot_lims[f"{axis}lim"])

        return self
