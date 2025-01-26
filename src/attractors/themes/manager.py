import json
import random
from pathlib import Path
from typing import ClassVar

from attractors.themes.theme import Theme


class ThemeManager:
    """
    Manager for loading and accessing visualization themes.

    Themes can be loaded from JSON files, added/removed programmatically,
    and accessed by name or randomly. A default theme is always available.

    Examples:
        >>> ThemeManager.load("themes.json")
        >>> theme = ThemeManager.get("dark")
        >>> ThemeManager.set_default("light")
        >>> random_theme = ThemeManager.random()
    """

    _themes: ClassVar[dict[str, Theme]] = {}
    _default_theme: ClassVar[str] = "ayu"

    @classmethod
    def load(cls, path: str | Path) -> None:
        """
        Load themes from JSON file.

        Args:
            path (str | Path): Path to JSON theme file
        """
        with open(path) as f:
            theme_data = json.load(f)

        for name, data in theme_data.items():
            cls._themes[name] = Theme(
                name=name,
                background=data["background"],
                colors=data["colors"],
                foreground=data.get("foreground", "#FFFFFF"),
            )

    @classmethod
    def get(cls, name: str | None = None) -> Theme:
        """
        Get theme by name or default.

        Args:
            name (str | None, optional): Theme name. Uses default if None. Defaults to None.

        Returns:
            Theme: Requested theme instance

        Raises:
            KeyError: If theme name not found
        """
        name = name or cls._default_theme
        if name not in cls._themes:
            msg = f"Theme '{name}' not found"
            raise KeyError(msg)
        return cls._themes[name]

    @classmethod
    def list_themes(cls) -> list[str]:
        """
        List available themes.

        Returns:
            list[str]: List of theme names
        """
        return list(cls._themes.keys())

    @classmethod
    def set_default(cls, name: str) -> None:
        """
        Set default theme.

        Args:
            name (str): Name of theme to set as default

        Raises:
            KeyError: If theme name not found
        """
        if name not in cls._themes:
            msg = f"Theme '{name}' not found"
            raise KeyError(msg)
        cls._default_theme = name

    @classmethod
    def add(cls, theme: Theme) -> None:
        """
        Add new theme.

        Args:
            theme (Theme): Theme instance to add
        """
        cls._themes[theme.name] = theme

    @classmethod
    def remove(cls, name: str) -> None:
        """
        Remove theme.

        Args:
            name (str): Name of theme to remove

        Raises:
            ValueError: If attempting to remove default theme
        """
        if name == cls._default_theme:
            raise ValueError("Cannot remove default theme")
        cls._themes.pop(name)

    @classmethod
    def random(cls) -> Theme:
        """
        Get random theme.

        Returns:
            Theme: Randomly selected theme instance
        """
        return random.choice(list(cls._themes.values()))  # noqa: S311
