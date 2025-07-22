"""
Tests for package integration with Sphinx and dependencies.
"""

from unittest.mock import Mock

from jsoncrack_for_sphinx import setup
from jsoncrack_for_sphinx.config import (
    ContainerConfig,
    JsonCrackConfig,
    RenderConfig,
    RenderMode,
)


class TestPackageIntegration:
    """Test package integration features."""

    def test_package_dependencies(self):
        """Test that package dependencies are available."""
        # Test that required dependencies can be imported

        # Test optional dependencies
        try:
            import jsf  # noqa: F401

            jsf_available = True
        except ImportError:
            jsf_available = False

        # jsf is listed as a dependency, so it should be available
        assert jsf_available, "jsf dependency should be available"

    def test_package_sphinx_integration(self):
        """Test that package integrates with Sphinx."""
        # Create mock Sphinx app
        mock_app = Mock()
        mock_app.config = Mock()
        mock_app.config.html_static_path = []
        mock_app.add_config_value = Mock()
        mock_app.add_directive = Mock()
        mock_app.connect = Mock()
        mock_app.add_css_file = Mock()
        mock_app.add_js_file = Mock()

        # Test that setup works
        result = setup(mock_app)

        # Verify setup result
        assert isinstance(result, dict)
        assert "version" in result
        assert result["version"] == "0.1.0"
        assert "parallel_read_safe" in result
        assert "parallel_write_safe" in result

    def test_package_config_classes(self):
        """Test that configuration classes work correctly."""
        # Test RenderConfig
        render_config = RenderConfig(mode=RenderMode.OnClick())
        assert hasattr(render_config, "mode")

        # Test ContainerConfig
        container_config = ContainerConfig()
        assert hasattr(container_config, "height")
        assert hasattr(container_config, "width")

        # Test JsonCrackConfig
        json_crack_config = JsonCrackConfig()
        assert hasattr(json_crack_config, "render")
        assert hasattr(json_crack_config, "container")

        # Test that configs can be created with parameters
        render_config_custom = RenderConfig(mode=RenderMode.OnLoad())
        assert render_config_custom.mode.mode == "onload"

        container_config_custom = ContainerConfig(height="500px", width="100%")
        assert container_config_custom.height == "500px"
        assert container_config_custom.width == "100%"

        # Test that combined config works
        combined_config = JsonCrackConfig(
            render=render_config_custom, container=container_config_custom
        )
        assert combined_config.render.mode.mode == "onload"
        assert combined_config.container.height == "500px"
