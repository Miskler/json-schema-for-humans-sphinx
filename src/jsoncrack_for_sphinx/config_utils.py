"""
Configuration utilities for the JSONCrack Sphinx extension.
"""

from typing import Any, Union

from .config_classes import ContainerConfig, RenderConfig
from .config_parser import JsonCrackConfig, parse_config
from .types import Directions, RenderMode, Theme


def get_jsoncrack_config(app_config: Any) -> JsonCrackConfig:
    """Get JSONCrack configuration from Sphinx app config."""

    # Try to get new-style config first
    if hasattr(app_config, "jsoncrack_default_options"):
        config_dict = app_config.jsoncrack_default_options
        return parse_config(config_dict)

    # Fall back to old-style config for backward compatibility
    # Parse render mode
    render_mode_str = getattr(app_config, "jsoncrack_render_mode", "onclick")
    render_mode: Union[RenderMode.OnClick, RenderMode.OnLoad, RenderMode.OnScreen]
    if render_mode_str == "onclick":
        render_mode = RenderMode.OnClick()
    elif render_mode_str == "onload":
        render_mode = RenderMode.OnLoad()
    elif render_mode_str == "onscreen":
        threshold = getattr(app_config, "jsoncrack_onscreen_threshold", 0.1)
        margin = getattr(app_config, "jsoncrack_onscreen_margin", "50px")
        render_mode = RenderMode.OnScreen(threshold=threshold, margin=margin)
    else:
        render_mode = RenderMode.OnClick()

    # Parse direction
    direction_str = getattr(app_config, "jsoncrack_direction", "RIGHT")
    direction = Directions(direction_str)

    # Parse theme
    theme_str = getattr(app_config, "jsoncrack_theme", None)
    if theme_str == "light":
        theme = Theme.LIGHT
    elif theme_str == "dark":
        theme = Theme.DARK
    else:
        theme = Theme.AUTO

    # Parse container settings
    height = getattr(app_config, "jsoncrack_height", "500")
    width = getattr(app_config, "jsoncrack_width", "100%")

    return JsonCrackConfig(
        render=RenderConfig(render_mode),
        container=ContainerConfig(direction=direction, height=height, width=width),
        theme=theme,
    )
