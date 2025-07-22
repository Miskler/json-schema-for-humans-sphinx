"""
Configuration classes for JSONCrack components.
"""

from typing import Union

from ..utils.types import Directions, RenderMode


class ContainerConfig:
    """Container configuration."""

    def __init__(
        self,
        direction: Directions = Directions.RIGHT,
        height: Union[int, str] = "500",
        width: Union[int, str] = "100%",
    ):
        """
        Args:
            direction: Visualization direction
            height: Container height in pixels or string
            width: Container width in pixels, percentage, or string
        """
        self.direction = direction
        self.height = str(height)
        self.width = str(width)

    def __repr__(self) -> str:
        return (
            f"ContainerConfig(direction={self.direction}, "
            f"height='{self.height}', width='{self.width}')"
        )


class RenderConfig:
    """Render configuration."""

    def __init__(
        self, mode: Union[RenderMode.OnClick, RenderMode.OnLoad, RenderMode.OnScreen]
    ):
        """
        Args:
            mode: Render mode instance
        """
        self.mode = mode

    def __repr__(self) -> str:
        return f"RenderConfig(mode={self.mode})"
