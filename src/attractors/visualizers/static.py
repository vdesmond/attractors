from typing import Any

from attractors.type_defs import Vector
from attractors.visualizers.base import BasePlotter


class StaticPlotter(BasePlotter):
    """Plotter for static visualization of dynamical system trajectories."""

    def visualize_impl(
        self,
        trajectory: Vector,
        line_kwargs: dict[str, Any] | None = None,
        segment_overlap: int = 1,
        **kwargs: Any,
    ) -> "StaticPlotter":
        """
        Create a static plot of trajectory segments with color mapping.

        Args:
            trajectory (Vector): Trajectory points to visualize
            line_kwargs (dict[str, Any] | None): Additional arguments for matplotlib line plots.
            segment_overlap (int): Number of points to overlap between segments. Defaults to 1.
            **kwargs (Any): Additional visualization parameters

        Returns:
            StaticPlotter: Self reference for method chaining
        """
        if line_kwargs is None:
            line_kwargs = {"linewidth": 1, "antialiased": True}

        self._setup_plot()

        line_kwargs = line_kwargs or {"linewidth": 1, "antialiased": True}

        n = len(trajectory)
        segment_size = n // self.num_segments
        overlap = segment_overlap

        segments = []
        color_values = self._get_color_values(trajectory)
        color_segments = []

        for i in range(self.num_segments):
            start_idx = max(0, i * segment_size - overlap)
            end_idx = min(n, (i + 1) * segment_size + overlap)
            segments.append(trajectory[start_idx:end_idx])
            color_segments.append(color_values[start_idx:end_idx])

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
