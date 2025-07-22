"""
Configuration value extraction utilities.
"""

from typing import Any, Dict

from ..utils.types import RenderMode, Theme
from .config_main import JsonCrackConfig


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
