"""
Integration tests for Sphinx build functionality.
"""

import json
from unittest.mock import Mock

import pytest

from jsoncrack_for_sphinx import setup
from jsoncrack_for_sphinx.generators.rst_generator import schema_to_rst


@pytest.mark.slow
class TestSphinxIntegration:
    """Integration tests that require Sphinx environment."""

    def test_sphinx_build_integration(self, temp_dir):
        """Test integration with actual Sphinx build process."""
        # This test would require setting up a full Sphinx environment
        # For now, we'll test the components that would be used in a build

        # Create a mock Sphinx application
        mock_app = Mock()
        mock_app.config = Mock()
        mock_app.config.html_static_path = []
        mock_app.env = Mock()

        # Set up extension
        result = setup(mock_app)

        # Verify setup was successful
        assert result["version"] == "0.1.0"
        assert result["parallel_read_safe"] is True
        assert result["parallel_write_safe"] is True

        # Verify configuration was added
        assert mock_app.add_config_value.called
        assert mock_app.add_directive.called
        assert mock_app.connect.called
        assert mock_app.add_css_file.called
        assert mock_app.add_js_file.called

    def test_rst_generation_integration(self, temp_dir):
        """Test RST generation integration."""
        # Create a complex schema for testing
        complex_schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "title": "Complex Integration Schema",
            "description": "A complex schema for integration testing",
            "properties": {
                "metadata": {
                    "type": "object",
                    "description": "Metadata information",
                    "properties": {
                        "created_at": {"type": "string", "format": "date-time"},
                        "updated_at": {"type": "string", "format": "date-time"},
                        "version": {
                            "type": "string",
                            "pattern": "^\\d+\\.\\d+\\.\\d+$",
                        },
                    },
                },
                "data": {
                    "type": "array",
                    "description": "Array of data objects",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "integer"},
                            "value": {"type": "string"},
                            "tags": {"type": "array", "items": {"type": "string"}},
                        },
                    },
                },
            },
            "required": ["metadata", "data"],
        }

        schema_file = temp_dir / "complex.schema.json"
        with open(schema_file, "w") as f:
            json.dump(complex_schema, f, indent=2)

        # Generate RST
        rst_content = schema_to_rst(schema_file, title="Complex Integration Test")

        # Verify RST structure
        assert "Complex Integration Test" in rst_content
        assert "=" * len("Complex Integration Test") in rst_content
        assert ".. raw:: html" in rst_content
        assert "json-schema-container" in rst_content

        # Verify the content can be processed by Sphinx
        lines = rst_content.split("\n")
        assert (
            len(lines) > 5
        )  # Should have title, separator, blank line, directive, content
        assert lines[0] == "Complex Integration Test"
        assert lines[1] == "=" * len("Complex Integration Test")
        assert lines[2] == ""
        assert lines[3] == ".. raw:: html"
