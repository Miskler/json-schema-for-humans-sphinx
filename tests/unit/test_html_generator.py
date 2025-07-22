"""
Tests for HTML generation functionality.
"""

from unittest.mock import Mock, patch

from jsoncrack_for_sphinx.config import (
    ContainerConfig,
    Directions,
    RenderConfig,
    RenderMode,
    Theme,
)
from jsoncrack_for_sphinx.generators.html_generator import generate_schema_html


class TestGenerateSchemaHtml:
    """Test generating schema HTML."""

    def test_generate_schema_html_schema_file(self, schema_file):
        """Test generating HTML for a schema file."""
        html_content = generate_schema_html(schema_file, "schema")

        assert "jsoncrack-container" in html_content
        assert "data-schema=" in html_content
        assert 'data-render-mode="onclick"' in html_content
        assert 'data-direction="RIGHT"' in html_content
        assert 'data-height="500"' in html_content
        assert 'data-width="100%"' in html_content

    def test_generate_schema_html_json_file(self, json_file):
        """Test generating HTML for a JSON data file."""
        html_content = generate_schema_html(json_file, "json")

        assert "jsoncrack-container" in html_content
        assert "data-schema=" in html_content
        # Should contain the actual JSON data
        assert "John Doe" in html_content or "john.doe@example.com" in html_content

    def test_generate_schema_html_with_config(self, schema_file):
        """Test generating HTML with custom configuration."""
        mock_config = Mock()
        mock_config.jsoncrack_default_options = {
            "render": RenderConfig(RenderMode.OnLoad()),
            "container": ContainerConfig(
                direction=Directions.LEFT, height="600", width="90%"
            ),
            "theme": Theme.DARK,
        }

        html_content = generate_schema_html(schema_file, "schema", mock_config)

        assert 'data-render-mode="onload"' in html_content
        assert 'data-direction="LEFT"' in html_content
        assert 'data-height="600"' in html_content
        assert 'data-width="90%"' in html_content
        assert 'data-theme="dark"' in html_content

    def test_generate_schema_html_invalid_file(self, temp_dir):
        """Test generating HTML for invalid schema file."""
        invalid_file = temp_dir / "invalid.schema.json"
        with open(invalid_file, "w") as f:
            f.write("invalid json")

        html_content = generate_schema_html(invalid_file, "schema")

        assert "error" in html_content.lower()
        assert "Error processing schema file" in html_content

    def test_generate_schema_html_with_jsf_available(self, schema_file):
        """Test generating HTML with JSF fake data generation when available."""
        # Mock JSF module import
        mock_jsf_module = Mock()
        mock_jsf_class = Mock()
        mock_jsf_instance = Mock()
        mock_jsf_instance.generate.return_value = {
            "name": "Fake Name",
            "email": "fake@example.com",
            "age": 25,
        }
        mock_jsf_class.return_value = mock_jsf_instance
        mock_jsf_module.JSF = mock_jsf_class

        with patch.dict("sys.modules", {"jsf": mock_jsf_module}):
            html_content = generate_schema_html(schema_file, "schema")

            assert "jsoncrack-container" in html_content
            # Should contain the fake data
            assert "Fake Name" in html_content or "fake@example.com" in html_content

    def test_generate_schema_html_jsf_import_error(self, schema_file):
        """Test generating HTML when JSF is not available."""
        with patch(
            "builtins.__import__", side_effect=ImportError("No module named 'jsf'")
        ):
            html_content = generate_schema_html(schema_file, "schema")

            # Should return error HTML when JSF import fails during schema processing
            assert "error" in html_content.lower()
            assert "Error processing schema file" in html_content

    def test_generate_schema_html_jsf_generation_error(self, schema_file):
        """Test generating HTML when JSF fails to generate data."""
        # Mock JSF module import but make generation fail
        mock_jsf_module = Mock()
        mock_jsf_class = Mock()
        mock_jsf_instance = Mock()
        mock_jsf_instance.generate.side_effect = Exception("JSF generation error")
        mock_jsf_class.return_value = mock_jsf_instance
        mock_jsf_module.JSF = mock_jsf_class

        with patch.dict("sys.modules", {"jsf": mock_jsf_module}):
            html_content = generate_schema_html(schema_file, "schema")

            assert "jsoncrack-container" in html_content
            # Should fall back to using the schema as-is
            assert "data-schema=" in html_content
