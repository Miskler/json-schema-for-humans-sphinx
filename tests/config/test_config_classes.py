"""
Tests for basic configuration classes and enums.
"""

from jsoncrack_for_sphinx.config import (
    ContainerConfig,
    Directions,
    RenderConfig,
    RenderMode,
    Theme,
)


class TestRenderMode:
    """Test render mode classes."""

    def test_onclick_mode(self):
        """Test OnClick render mode."""
        mode = RenderMode.OnClick()
        assert mode.mode == "onclick"
        assert repr(mode) == "RenderMode.OnClick()"

    def test_onload_mode(self):
        """Test OnLoad render mode."""
        mode = RenderMode.OnLoad()
        assert mode.mode == "onload"
        assert repr(mode) == "RenderMode.OnLoad()"

    def test_onscreen_mode_default(self):
        """Test OnScreen render mode with default values."""
        mode = RenderMode.OnScreen()
        assert mode.mode == "onscreen"
        assert mode.threshold == 0.1
        assert mode.margin == "50px"
        assert repr(mode) == "RenderMode.OnScreen(threshold=0.1, margin='50px')"

    def test_onscreen_mode_custom(self):
        """Test OnScreen render mode with custom values."""
        mode = RenderMode.OnScreen(threshold=0.3, margin="100px")
        assert mode.mode == "onscreen"
        assert mode.threshold == 0.3
        assert mode.margin == "100px"
        assert repr(mode) == "RenderMode.OnScreen(threshold=0.3, margin='100px')"


class TestDirections:
    """Test direction enum."""

    def test_direction_values(self):
        """Test all direction values."""
        assert Directions.TOP.value == "TOP"
        assert Directions.RIGHT.value == "RIGHT"
        assert Directions.DOWN.value == "DOWN"
        assert Directions.LEFT.value == "LEFT"


class TestTheme:
    """Test theme enum."""

    def test_theme_values(self):
        """Test all theme values."""
        assert Theme.LIGHT.value == "light"
        assert Theme.DARK.value == "dark"
        assert Theme.AUTO.value is None


class TestContainerConfig:
    """Test container configuration."""

    def test_default_container_config(self):
        """Test default container configuration."""
        config = ContainerConfig()
        assert config.direction == Directions.RIGHT
        assert config.height == "500"
        assert config.width == "100%"
        assert "RIGHT" in repr(config)
        assert "height" in repr(config)

    def test_custom_container_config(self):
        """Test custom container configuration."""
        config = ContainerConfig(direction=Directions.LEFT, height=400, width="80%")
        assert config.direction == Directions.LEFT
        assert config.height == "400"
        assert config.width == "80%"

    def test_container_config_int_values(self):
        """Test container configuration with integer values."""
        config = ContainerConfig(height=600, width=800)
        assert config.height == "600"
        assert config.width == "800"


class TestRenderConfig:
    """Test render configuration."""

    def test_render_config_onclick(self):
        """Test render configuration with OnClick mode."""
        mode = RenderMode.OnClick()
        config = RenderConfig(mode)
        assert config.mode is mode
        assert "OnClick" in repr(config)

    def test_render_config_onload(self):
        """Test render configuration with OnLoad mode."""
        mode = RenderMode.OnLoad()
        config = RenderConfig(mode)
        assert config.mode is mode
        assert "OnLoad" in repr(config)

    def test_render_config_onscreen(self):
        """Test render configuration with OnScreen mode."""
        mode = RenderMode.OnScreen(threshold=0.2, margin="75px")
        config = RenderConfig(mode)
        assert config.mode is mode
        assert "OnScreen" in repr(config)
