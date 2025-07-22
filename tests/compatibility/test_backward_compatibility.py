"""
Backward compatibility tests.
"""

from unittest.mock import Mock

from jsoncrack_for_sphinx.config import RenderMode


class TestBackwardCompatibility:
    """Test backward compatibility with older configurations."""

    def test_legacy_config_format(self):
        """Test that legacy configuration format still works."""
        from jsoncrack_for_sphinx.config.config_utils import get_jsoncrack_config

        # Create old-style configuration
        mock_config = Mock()
        # Remove new-style config
        if hasattr(mock_config, "jsoncrack_default_options"):
            delattr(mock_config, "jsoncrack_default_options")

        # Set old-style config values
        mock_config.jsoncrack_render_mode = "onclick"
        mock_config.jsoncrack_theme = "dark"
        mock_config.jsoncrack_direction = "LEFT"
        mock_config.jsoncrack_height = "600"
        mock_config.jsoncrack_width = "90%"
        mock_config.jsoncrack_onscreen_threshold = 0.2
        mock_config.jsoncrack_onscreen_margin = "75px"

        # Should still work
        config = get_jsoncrack_config(mock_config)

        assert config is not None
        assert config.theme.value == "dark"
        assert config.container.height == "600"
        assert config.container.width == "90%"

    def test_partial_legacy_config(self):
        """Test partial legacy configuration."""
        from jsoncrack_for_sphinx.config.config_utils import get_jsoncrack_config

        mock_config = Mock()
        if hasattr(mock_config, "jsoncrack_default_options"):
            delattr(mock_config, "jsoncrack_default_options")

        # Set only some old-style values
        mock_config.jsoncrack_render_mode = "onscreen"
        mock_config.jsoncrack_direction = "DOWN"
        mock_config.jsoncrack_theme = None
        mock_config.jsoncrack_height = "500"
        mock_config.jsoncrack_width = "100%"
        mock_config.jsoncrack_onscreen_threshold = 0.1
        mock_config.jsoncrack_onscreen_margin = "50px"

        config = get_jsoncrack_config(mock_config)

        assert isinstance(config.render.mode, RenderMode.OnScreen)
        assert config.container.direction.value == "DOWN"
        assert config.container.height == "500"
