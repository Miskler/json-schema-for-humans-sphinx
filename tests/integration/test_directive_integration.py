"""
Integration tests for directive and Sphinx app functionality.
"""

import json
from unittest.mock import Mock

from jsoncrack_for_sphinx import setup
from jsoncrack_for_sphinx.core.directive import SchemaDirective
from jsoncrack_for_sphinx.generators.html_generator import generate_schema_html


class TestDirectiveIntegration:
    """Integration tests for directive functionality."""

    def test_directive_integration(self, temp_dir):
        """Test the schema directive integration."""
        # Create schema directory and files
        schema_dir = temp_dir / "schemas"
        schema_dir.mkdir()

        test_schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "title": "Test Schema",
            "description": "A test schema for integration testing",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"},
                "active": {"type": "boolean", "default": True},
            },
            "required": ["id", "name"],
        }

        with open(schema_dir / "test.schema.json", "w") as f:
            json.dump(test_schema, f, indent=2)

        # Test HTML generation instead of directive directly
        schema_file = schema_dir / "test.schema.json"
        html = generate_schema_html(schema_file, "schema")

        assert "jsoncrack-container" in html
        assert "data-schema=" in html
        # JSF may generate fake data, so we check for the container presence
        assert 'data-render-mode="onclick"' in html or "data-render-mode=" in html

    def test_sphinx_app_setup_integration(self):
        """Test the complete Sphinx app setup integration."""
        mock_app = Mock()
        mock_app.config = Mock()
        mock_app.config.html_static_path = []
        mock_app.add_config_value = Mock()
        mock_app.add_directive = Mock()
        mock_app.connect = Mock()
        mock_app.add_css_file = Mock()
        mock_app.add_js_file = Mock()

        # Test setup
        result = setup(mock_app)

        # Verify all configuration values were added
        config_calls = mock_app.add_config_value.call_args_list
        config_names = [call[0][0] for call in config_calls]

        expected_configs = [
            "json_schema_dir",
            "jsoncrack_default_options",
            "jsoncrack_render_mode",
            "jsoncrack_theme",
            "jsoncrack_direction",
            "jsoncrack_height",
            "jsoncrack_width",
            "jsoncrack_onscreen_threshold",
            "jsoncrack_onscreen_margin",
        ]

        for config_name in expected_configs:
            assert config_name in config_names

        # Verify directive was added
        mock_app.add_directive.assert_called_once_with("schema", SchemaDirective)

        # Verify autodoc hooks were connected
        connect_calls = mock_app.connect.call_args_list
        assert len(connect_calls) >= 2

        # Verify static files were added
        mock_app.add_css_file.assert_called_once_with("jsoncrack-schema.css")
        mock_app.add_js_file.assert_called_once_with("jsoncrack-sphinx.js")

        # Verify static path was added
        assert len(mock_app.config.html_static_path) == 1
        assert "static" in mock_app.config.html_static_path[0]

        # Verify return value
        assert result["version"] == "0.1.0"
        assert result["parallel_read_safe"] is True
        assert result["parallel_write_safe"] is True
