from dataclasses import dataclass

import matplotlib.colors


@dataclass(frozen=True)
class Theme:
    """
    Immutable theme data class for visualization styling.

    Attributes:
        name (str): Theme identifier
        background (str): Background color in hex format
        foreground (str): Foreground color in hex format
        colors (str | list[str]): Either matplotlib colormap name or list of hex colors
    """

    name: str
    background: str
    foreground: str
    colors: str | list[str]

    @property
    def colormap(self) -> matplotlib.colors.Colormap:
        """
        Get matplotlib colormap for theme colors.

        Returns:
            matplotlib.colors.Colormap: Generated colormap from theme colors
        """
        if isinstance(self.colors, str):
            return matplotlib.colormaps[self.colors]
        rgb_colors = [
            tuple(int(c.lstrip("#")[i : i + 2], 16) / 255 for i in (0, 2, 4)) for c in self.colors
        ]
        return matplotlib.colors.LinearSegmentedColormap.from_list(self.name, rgb_colors)
