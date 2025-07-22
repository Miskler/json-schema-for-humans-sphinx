"""
Integration tests for HTML generation and JSF functionality.
"""

import json
from unittest.mock import Mock, patch

from jsoncrack_for_sphinx.generators.html_generator import generate_schema_html


class TestHtmlGenerationIntegration:
    """Integration tests for HTML generation."""

    def test_html_generation_integration(self, temp_dir):
        """Test HTML generation integration."""
        # Create schema file
        schema_data = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "title": "Integration Test",
            "properties": {
                "user_id": {"type": "integer"},
                "username": {"type": "string"},
                "profile": {
                    "type": "object",
                    "properties": {
                        "email": {"type": "string", "format": "email"},
                        "age": {"type": "integer", "minimum": 0},
                    },
                },
            },
            "required": ["user_id", "username"],
        }

        schema_file = temp_dir / "integration.schema.json"
        with open(schema_file, "w") as f:
            json.dump(schema_data, f)

        # Create JSON file
        json_data = {
            "user_id": 123,
            "username": "testuser",
            "profile": {"email": "test@example.com", "age": 25},
        }

        json_file = temp_dir / "integration.json"
        with open(json_file, "w") as f:
            json.dump(json_data, f)

        # Test schema HTML generation
        schema_html = generate_schema_html(schema_file, "schema")

        assert "jsoncrack-container" in schema_html
        assert "data-schema=" in schema_html
        assert 'data-render-mode="onclick"' in schema_html

        # Test JSON HTML generation
        json_html = generate_schema_html(json_file, "json")

        assert "jsoncrack-container" in json_html
        assert "data-schema=" in json_html
        assert "testuser" in json_html
        assert "test@example.com" in json_html

    @patch("jsf.JSF")
    def test_jsf_integration(self, mock_jsf, temp_dir):
        """Test integration with JSF fake data generation."""
        # Mock JSF to return fake data
        mock_jsf_instance = Mock()
        mock_jsf_instance.generate.return_value = {
            "user_id": 999,
            "username": "generated_user",
            "profile": {"email": "generated@example.com", "age": 35},
        }
        mock_jsf.return_value = mock_jsf_instance

        # Create schema file
        schema_data = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "title": "JSF Test",
            "properties": {
                "user_id": {"type": "integer"},
                "username": {"type": "string"},
                "profile": {
                    "type": "object",
                    "properties": {
                        "email": {"type": "string", "format": "email"},
                        "age": {"type": "integer"},
                    },
                },
            },
        }

        schema_file = temp_dir / "jsf_test.schema.json"
        with open(schema_file, "w") as f:
            json.dump(schema_data, f)

        # Generate HTML
        html = generate_schema_html(schema_file, "schema")

        # Verify JSF was called
        mock_jsf.assert_called_once_with(schema_data)
        mock_jsf_instance.generate.assert_called_once()

        # Verify generated data is in HTML
        assert "generated_user" in html
        assert "generated@example.com" in html

    def test_error_handling_integration(self, temp_dir):
        """Test error handling integration."""
        # Create invalid JSON file
        invalid_file = temp_dir / "invalid.schema.json"
        with open(invalid_file, "w") as f:
            f.write("invalid json content")

        # Test error handling
        html = generate_schema_html(invalid_file, "schema")

        assert "error" in html.lower()
        assert "Error processing schema file" in html

        # Test non-existent file
        non_existent = temp_dir / "non_existent.schema.json"
        html = generate_schema_html(non_existent, "schema")

        assert "error" in html.lower()
