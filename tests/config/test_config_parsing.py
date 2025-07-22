"""
Tests for JsonCrackConfig and parsing functionality.
"""

from jsoncrack_for_sphinx.config import (
    ContainerConfig,
    Directions,
    JsonCrackConfig,
    RenderConfig,
    RenderMode,
    Theme,
    get_config_values,
    parse_config,
)


class TestJsonCrackConfig:
    """Test main JSONCrack configuration."""

    def test_default_config(self):
        """Test default configuration."""
        config = JsonCrackConfig()
        assert isinstance(config.render.mode, RenderMode.OnClick)
        assert config.container.direction == Directions.RIGHT
        assert config.container.height == "500"
        assert config.container.width == "100%"
        assert config.theme == Theme.AUTO
        assert config.disable_autodoc is False
        assert config.autodoc_ignore == []

    def test_custom_config(self):
        """Test custom configuration."""
        render_config = RenderConfig(RenderMode.OnLoad())
        container_config = ContainerConfig(
            direction=Directions.DOWN, height="400", width="90%"
        )

        config = JsonCrackConfig(
            render=render_config, container=container_config, theme=Theme.DARK
        )

        assert config.render == render_config
        assert config.container == container_config
        assert config.theme == Theme.DARK

    def test_config_with_none_values(self):
        """Test configuration with None values (should use defaults)."""
        config = JsonCrackConfig(render=None, container=None)
        assert isinstance(config.render.mode, RenderMode.OnClick)
        assert config.container.direction == Directions.RIGHT
        assert config.theme == Theme.AUTO

    def test_config_repr(self):
        """Test configuration string representation."""
        config = JsonCrackConfig()
        repr_str = repr(config)
        assert "JsonCrackConfig" in repr_str
        assert "render" in repr_str
        assert "container" in repr_str
        assert "theme" in repr_str

    def test_custom_config_with_autodoc_settings(self):
        """Test custom configuration with autodoc settings."""
        config = JsonCrackConfig(
            disable_autodoc=True,
            autodoc_ignore=["test.module", "examples."],
        )
        assert config.disable_autodoc is True
        assert config.autodoc_ignore == ["test.module", "examples."]


class TestParseConfig:
    """Test configuration parsing."""

    def test_parse_empty_config(self):
        """Test parsing empty configuration."""
        config = parse_config({})
        assert isinstance(config, JsonCrackConfig)
        assert isinstance(config.render.mode, RenderMode.OnClick)

    def test_parse_dict_config(self):
        """Test parsing dictionary configuration."""
        config_dict = {
            "render": {"mode": "onload"},
            "container": {"direction": "LEFT", "height": "600"},
            "theme": "dark",
        }

        config = parse_config(config_dict)
        assert isinstance(config.render.mode, RenderMode.OnLoad)
        assert config.container.direction == Directions.LEFT
        assert config.container.height == "600"
        assert config.theme == Theme.DARK

    def test_parse_nested_config(self):
        """Test parsing nested configuration."""
        config_dict = {
            "render": {
                "mode": {"type": "onscreen", "threshold": 0.3, "margin": "100px"}
            },
            "container": {"direction": "TOP", "height": 300, "width": "80%"},
        }

        config = parse_config(config_dict)
        assert isinstance(config.render.mode, RenderMode.OnScreen)
        assert config.render.mode.threshold == 0.3
        assert config.render.mode.margin == "100px"
        assert config.container.direction == Directions.TOP
        assert config.container.height == "300"
        assert config.container.width == "80%"

    def test_parse_invalid_values(self):
        """Test parsing configuration with invalid values."""
        config_dict = {
            "container": {"direction": "INVALID", "height": "invalid"},
            "theme": "invalid_theme",
        }

        config = parse_config(config_dict)
        # Should fallback to defaults for invalid values
        assert config.container.direction == Directions.RIGHT  # default
        assert config.container.height == "invalid"  # passed through as string
        assert config.theme == Theme.AUTO  # default for invalid

    def test_parse_config_with_autodoc_settings(self):
        """Test parsing configuration with autodoc settings."""
        config_dict = {
            "disable_autodoc": True,
            "autodoc_ignore": ["mymodule.test", "examples."],
        }

        config = parse_config(config_dict)
        assert config.disable_autodoc is True
        assert config.autodoc_ignore == ["mymodule.test", "examples."]

    def test_parse_config_without_autodoc_settings(self):
        """Test parsing configuration without autodoc settings (uses defaults)."""
        config_dict = {}

        config = parse_config(config_dict)
        assert config.disable_autodoc is False
        assert config.autodoc_ignore == []


class TestGetConfigValues:
    """Test getting configuration values."""

    def test_get_config_values_default(self):
        """Test getting default configuration values."""
        config = JsonCrackConfig()  # Create default config
        values = get_config_values(config)

        # These are the actual config values returned by get_config_values
        assert "render_mode" in values
        assert "theme" in values
        assert "direction" in values
        assert "height" in values
        assert "width" in values
        assert "onscreen_threshold" in values
        assert "onscreen_margin" in values

        # Check default values
        assert values["render_mode"] == "onclick"
        assert values["theme"] is None
        assert values["direction"] == "RIGHT"
        assert values["height"] == "500"
        assert values["width"] == "100%"
        assert values["onscreen_threshold"] == 0.1
        assert values["onscreen_margin"] == "50px"
