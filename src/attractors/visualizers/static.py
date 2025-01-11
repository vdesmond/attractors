from typing import Any

import numpy as np

from attractors.type_defs import Vector
from attractors.visualizers.base import BasePlotter


class StaticPlotter(BasePlotter):
    def visualize(
        self,
        trajectory: Vector,
        line_kwargs: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> "StaticPlotter":
        self._setup_plot()
        line_kwargs = line_kwargs or {}
        segments = np.array_split(trajectory, self.num_segments)
        color_values = self._get_color_values(trajectory)
        color_segments = np.array_split(color_values, self.num_segments)

        for segment, color_segment in zip(segments, color_segments, strict=False):
            self.ax.plot(
                segment[:, 0],
                segment[:, 1],
                segment[:, 2],
                "-",
                c=self.theme.colormap(color_segment.mean()),
                **line_kwargs,
            )
        return self
