"""
Tests for configuration utilities.
"""

from unittest.mock import Mock

from jsoncrack_for_sphinx.config import (
    ContainerConfig,
    Directions,
    RenderConfig,
    RenderMode,
    Theme,
)
from jsoncrack_for_sphinx.config.config_utils import get_jsoncrack_config


class TestGetJsoncrackConfig:
    """Test getting JSONCrack configuration from app config."""

    def test_get_config_new_style(self):
        """Test getting new-style configuration."""
        app_config = Mock()
        app_config.jsoncrack_default_options = {
            "render": RenderConfig(RenderMode.OnLoad()),
            "container": ContainerConfig(
                direction=Directions.LEFT, height="600", width="90%"
            ),
            "theme": Theme.DARK,
        }

        config = get_jsoncrack_config(app_config)

        assert isinstance(config.render.mode, RenderMode.OnLoad)
        assert config.container.direction == Directions.LEFT
        assert config.container.height == "600"
        assert config.container.width == "90%"
        assert config.theme == Theme.DARK

    def test_get_config_old_style(self):
        """Test getting old-style configuration."""
        app_config = Mock()
        # Remove new-style config
        (
            delattr(app_config, "jsoncrack_default_options")
            if hasattr(app_config, "jsoncrack_default_options")
            else None
        )

        # Set old-style config
        app_config.jsoncrack_render_mode = "onscreen"
        app_config.jsoncrack_direction = "TOP"
        app_config.jsoncrack_theme = "light"
        app_config.jsoncrack_height = "700"
        app_config.jsoncrack_width = "80%"
        app_config.jsoncrack_onscreen_threshold = 0.3
        app_config.jsoncrack_onscreen_margin = "100px"

        config = get_jsoncrack_config(app_config)

        assert isinstance(config.render.mode, RenderMode.OnScreen)
        assert config.render.mode.threshold == 0.3
        assert config.render.mode.margin == "100px"
        assert config.container.direction == Directions.TOP
        assert config.container.height == "700"
        assert config.container.width == "80%"
        assert config.theme == Theme.LIGHT

    def test_get_config_old_style_defaults(self):
        """Test getting old-style configuration with default values."""
        app_config = Mock()
        (
            delattr(app_config, "jsoncrack_default_options")
            if hasattr(app_config, "jsoncrack_default_options")
            else None
        )

        # Set only some values, others should use defaults
        app_config.jsoncrack_render_mode = "onclick"
        app_config.jsoncrack_direction = "RIGHT"
        app_config.jsoncrack_theme = None
        app_config.jsoncrack_height = "500"
        app_config.jsoncrack_width = "100%"
        app_config.jsoncrack_onscreen_threshold = 0.1
        app_config.jsoncrack_onscreen_margin = "50px"

        config = get_jsoncrack_config(app_config)

        assert isinstance(config.render.mode, RenderMode.OnClick)
        assert config.container.direction == Directions.RIGHT
        assert config.theme == Theme.AUTO
