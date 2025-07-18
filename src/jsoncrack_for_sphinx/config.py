"""
Configuration classes for JSONCrack Sphinx extension.
"""

from enum import Enum
from typing import Any, Dict, Union


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


class JsonCrackConfig:
    """Main JSONCrack configuration."""

    def __init__(
        self,
        render: Union[RenderConfig, None] = None,
        container: Union[ContainerConfig, None] = None,
        theme: Theme = Theme.AUTO,
    ):
        """
        Args:
            render: Render configuration
            container: Container configuration
            theme: Theme setting
        """
        self.render = render or RenderConfig(RenderMode.OnClick())
        self.container = container or ContainerConfig()
        self.theme = theme

    def __repr__(self) -> str:
        return (
            f"JsonCrackConfig(render={self.render}, "
            f"container={self.container}, theme={self.theme})"
        )


def parse_config(config_dict: Dict[str, Any]) -> JsonCrackConfig:
    """Parse configuration dictionary into JsonCrackConfig object."""

    # Parse render config
    render_config = None
    if "render" in config_dict:
        render_obj = config_dict["render"]
        if isinstance(render_obj, RenderConfig):
            render_config = render_obj
        elif isinstance(render_obj, dict) and "mode" in render_obj:
            # Legacy format support
            mode_obj = render_obj["mode"]
            render_config = RenderConfig(mode_obj)

    # Parse container config
    container_config = None
    if "container" in config_dict:
        container_obj = config_dict["container"]
        if isinstance(container_obj, ContainerConfig):
            container_config = container_obj
        elif isinstance(container_obj, dict):
            # Legacy format support
            container_config = ContainerConfig(
                direction=container_obj.get("direction", Directions.RIGHT),
                height=container_obj.get("height", "500"),
                width=container_obj.get("width", "100%"),
            )

    # Parse theme
    theme = config_dict.get("theme", Theme.AUTO)

    return JsonCrackConfig(
        render=render_config or RenderConfig(RenderMode.OnClick()),
        container=container_config or ContainerConfig(),
        theme=theme,
    )


def get_config_values(config: JsonCrackConfig) -> Dict[str, Any]:
    """Extract configuration values for HTML generation."""

    # Get render mode settings
    render_mode = config.render.mode.mode
    onscreen_threshold = 0.1
    onscreen_margin = "50px"

    # Only get threshold and margin for OnScreen mode
    if isinstance(config.render.mode, RenderMode.OnScreen):
        onscreen_threshold = config.render.mode.threshold
        onscreen_margin = config.render.mode.margin

    # Get theme value
    theme_value = config.theme.value if config.theme != Theme.AUTO else None

    return {
        "render_mode": render_mode,
        "theme": theme_value,
        "direction": config.container.direction.value,
        "height": config.container.height,
        "width": config.container.width,
        "onscreen_threshold": onscreen_threshold,
        "onscreen_margin": onscreen_margin,
    }
