"""
Enums and basic types for configuration.
"""

from enum import Enum


class RenderMode:
    """Render mode configuration classes."""

    class OnClick:
        """Click to load mode - loads when user clicks the button."""

        def __init__(self) -> None:
            self.mode = "onclick"

        def __repr__(self) -> str:
            return "RenderMode.OnClick()"

    class OnLoad:
        """Immediate load mode - loads when page loads."""

        def __init__(self) -> None:
            self.mode = "onload"

        def __repr__(self) -> str:
            return "RenderMode.OnLoad()"

    class OnScreen:
        """Viewport load mode - loads when element becomes visible."""

        def __init__(self, threshold: float = 0.1, margin: str = "50px") -> None:
            """
            Args:
                threshold: Visibility threshold (0.0-1.0)
                margin: Root margin for early loading (e.g., '50px')
            """
            self.mode = "onscreen"
            self.threshold = threshold
            self.margin = margin

        def __repr__(self) -> str:
            return (
                f"RenderMode.OnScreen(threshold={self.threshold}, "
                f"margin='{self.margin}')"
            )


class Directions(Enum):
    """JSONCrack visualization directions."""

    TOP = "TOP"
    RIGHT = "RIGHT"
    DOWN = "DOWN"
    LEFT = "LEFT"


class Theme(Enum):
    """Theme options."""

    LIGHT = "light"
    DARK = "dark"
    AUTO = None  # Auto-detect from page


class PathSeparator(Enum):
    """Path separator options for schema file search."""

    DOT = "."  # Use dots: Class.method.schema.json
    SLASH = "/"  # Use slashes: Class/method.schema.json
    NONE = "none"  # No separator: Classmethod.schema.json
