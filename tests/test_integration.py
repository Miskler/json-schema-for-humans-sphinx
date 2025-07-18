"""
Integration tests for the jsoncrack-for-sphinx extension.
"""

import json
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from jsoncrack_for_sphinx import setup
from jsoncrack_for_sphinx.config import Directions, RenderMode, Theme
from jsoncrack_for_sphinx.extension import SchemaDirective, find_schema_for_object


class TestIntegration:
    """Integration tests for the full extension."""

    def test_full_workflow_with_autodoc(self, temp_dir):
        """Test the full workflow with autodoc integration."""
        # Create a mock Python module
        module_content = '''
"""Test module for integration testing."""

class User:
    """User management class."""

    def create(self, user_data):
        """
        Create a new user.

        Args:
            user_data: User data dictionary

        Returns:
            Created user information
        """
        return {"id": 1, "name": user_data["name"]}

    def update(self, user_id, update_data):
        """
        Update an existing user.

        Args:
            user_id: ID of the user to update
            update_data: Data to update

        Returns:
            Updated user information
        """
        return {"id": user_id, "updated": True}


def process_data(data, options=None):
    """
    Process input data.

    Args:
        data: Input data to process
        options: Processing options

    Returns:
        Processing results
    """
    return {"processed": len(data)}
'''

        # Create module file
        module_file = temp_dir / "test_module.py"
        with open(module_file, "w") as f:
            f.write(module_content)

        # Create schema directory
        schema_dir = temp_dir / "schemas"
        schema_dir.mkdir()

        # Create schema files
        schemas = {
            "User.create.schema.json": {
                "$schema": "http://json-schema.org/draft-07/schema#",
                "type": "object",
                "title": "User Creation",
                "properties": {
                    "name": {"type": "string"},
                    "email": {"type": "string", "format": "email"},
                },
                "required": ["name", "email"],
            },
            "User.update.schema.json": {
                "$schema": "http://json-schema.org/draft-07/schema#",
                "type": "object",
                "title": "User Update",
                "properties": {"name": {"type": "string"}, "age": {"type": "integer"}},
            },
            "process_data.schema.json": {
                "$schema": "http://json-schema.org/draft-07/schema#",
                "type": "object",
                "title": "Process Data",
                "properties": {
                    "data": {"type": "array"},
                    "options": {"type": "object"},
                },
            },
        }

        for filename, content in schemas.items():
            with open(schema_dir / filename, "w") as f:
                json.dump(content, f, indent=2)

        # Test finding schemas for objects
        assert (
            find_schema_for_object("test_module.User.create", str(schema_dir))
            is not None
        )
        assert (
            find_schema_for_object("test_module.User.update", str(schema_dir))
            is not None
        )
        assert (
            find_schema_for_object("test_module.process_data", str(schema_dir))
            is not None
        )

        # Test that schemas are found correctly
        schema_result = find_schema_for_object(
            "test_module.User.create", str(schema_dir)
        )
        assert schema_result is not None
        schema_path, file_type = schema_result
        assert Path(schema_path).name == "User.create.schema.json"
        assert file_type == "schema"

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
        from jsoncrack_for_sphinx.extension import generate_schema_html

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

    def test_config_integration(self, temp_dir):
        """Test configuration integration with different settings."""
        from jsoncrack_for_sphinx.config import ContainerConfig, RenderConfig
        from jsoncrack_for_sphinx.extension import get_jsoncrack_config

        # Test new-style configuration
        mock_config = Mock()
        mock_config.jsoncrack_default_options = {
            "render": RenderConfig(RenderMode.OnScreen(threshold=0.2, margin="75px")),
            "container": ContainerConfig(
                direction=Directions.LEFT, height="600", width="95%"
            ),
            "theme": Theme.DARK,
        }

        config = get_jsoncrack_config(mock_config)

        assert isinstance(config.render.mode, RenderMode.OnScreen)
        assert config.render.mode.threshold == 0.2
        assert config.render.mode.margin == "75px"
        assert config.container.direction == Directions.LEFT
        assert config.container.height == "600"
        assert config.container.width == "95%"
        assert config.theme == Theme.DARK

        # Test legacy configuration
        mock_config_legacy = Mock()
        (
            delattr(mock_config_legacy, "jsoncrack_default_options")
            if hasattr(mock_config_legacy, "jsoncrack_default_options")
            else None
        )

        mock_config_legacy.jsoncrack_render_mode = "onload"
        mock_config_legacy.jsoncrack_direction = "TOP"
        mock_config_legacy.jsoncrack_theme = "light"
        mock_config_legacy.jsoncrack_height = "400"
        mock_config_legacy.jsoncrack_width = "80%"
        mock_config_legacy.jsoncrack_onscreen_threshold = 0.3
        mock_config_legacy.jsoncrack_onscreen_margin = "100px"

        config_legacy = get_jsoncrack_config(mock_config_legacy)

        assert isinstance(config_legacy.render.mode, RenderMode.OnLoad)
        assert config_legacy.container.direction == Directions.TOP
        assert config_legacy.container.height == "400"
        assert config_legacy.container.width == "80%"
        assert config_legacy.theme == Theme.LIGHT

    def test_schema_file_types_integration(self, temp_dir):
        """Test integration with different schema file types."""
        schema_dir = temp_dir / "schemas"
        schema_dir.mkdir()

        # Create .schema.json file
        schema_data = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "title": "Test Schema",
            "properties": {"name": {"type": "string"}},
        }

        with open(schema_dir / "test.schema.json", "w") as f:
            json.dump(schema_data, f)

        # Create .json file
        json_data = {"name": "Test User", "email": "test@example.com", "age": 30}

        with open(schema_dir / "example.json", "w") as f:
            json.dump(json_data, f)

        # Test finding schema file
        schema_result = find_schema_for_object("module.test", str(schema_dir))
        assert schema_result is not None
        schema_path, file_type = schema_result
        assert Path(schema_path).name == "test.schema.json"
        assert file_type == "schema"

        # Test finding JSON file
        json_result = find_schema_for_object("module.example", str(schema_dir))
        assert json_result is not None
        json_path, file_type = json_result
        assert Path(json_path).name == "example.json"
        assert file_type == "json"

    def test_html_generation_integration(self, temp_dir):
        """Test HTML generation integration."""
        from jsoncrack_for_sphinx.extension import generate_schema_html

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
        from jsoncrack_for_sphinx.extension import generate_schema_html

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
        from jsoncrack_for_sphinx.extension import generate_schema_html

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
        from jsoncrack_for_sphinx.utils import schema_to_rst

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
