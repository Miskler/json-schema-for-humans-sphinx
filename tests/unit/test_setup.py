"""
Tests for extension setup functionality.
"""

from unittest.mock import Mock

from jsoncrack_for_sphinx.core.directive import SchemaDirective
from jsoncrack_for_sphinx.core.extension import setup


class TestSetup:
    """Test the setup function."""

    def test_setup_function(self):
        """Test the setup function registers everything correctly."""
        mock_app = Mock()
        mock_app.config = Mock()
        mock_app.config.html_static_path = []

        result = setup(mock_app)

        # Should add config values
        assert mock_app.add_config_value.call_count >= 8

        # Should add directive
        mock_app.add_directive.assert_called_once_with("schema", SchemaDirective)

        # Should connect to autodoc events
        assert mock_app.connect.call_count >= 2

        # Should add CSS and JS files
        mock_app.add_css_file.assert_called_once_with("jsoncrack-schema.css")
        mock_app.add_js_file.assert_called_once_with("jsoncrack-sphinx.js")

        # Should return correct metadata
        assert result["version"] == "0.1.0"
        assert result["parallel_read_safe"] is True
        assert result["parallel_write_safe"] is True

    def test_setup_adds_static_path(self):
        """Test that setup adds static path to config."""
        mock_app = Mock()
        mock_app.config = Mock()
        mock_app.config.html_static_path = []

        setup(mock_app)

        # Should add static path
        assert len(mock_app.config.html_static_path) == 1
        assert "static" in mock_app.config.html_static_path[0]
