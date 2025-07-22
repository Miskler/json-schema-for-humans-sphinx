"""
Tests for documentation examples and consistency.
"""

import json
from pathlib import Path

from jsoncrack_for_sphinx.config import (
    ContainerConfig,
    Directions,
    JsonCrackConfig,
    RenderConfig,
    RenderMode,
    Theme,
)


class TestDocumentationExamples:
    """Test key examples from documentation."""

    def test_readme_quick_start_example(self):
        """Test the quick start example from README."""
        # Test configuration example from README
        extensions = [
            "sphinx.ext.autodoc",
            "jsoncrack_for_sphinx",
        ]

        assert "jsoncrack_for_sphinx" in extensions
        assert "sphinx.ext.autodoc" in extensions

    def test_readme_file_naming_convention(self, temp_dir):
        """Test the file naming convention from README."""
        # Test the naming patterns mentioned in README
        schema_patterns = ["MyClass.my_method.schema.json", "my_function.schema.json"]

        # Create test files following the patterns
        for pattern in schema_patterns:
            schema_file = temp_dir / pattern
            with open(schema_file, "w") as f:
                json.dump({"type": "object", "title": "Test"}, f)

            assert schema_file.exists()

    def test_configuration_examples(self):
        """Test configuration examples."""
        # Test new-style configuration
        config = JsonCrackConfig(
            render=RenderConfig(RenderMode.OnScreen(threshold=0.2, margin="75px")),
            container=ContainerConfig(
                direction=Directions.LEFT, height="600", width="95%"
            ),
            theme=Theme.DARK,
        )

        assert isinstance(config.render.mode, RenderMode.OnScreen)
        assert config.render.mode.threshold == 0.2
        assert config.container.direction == Directions.LEFT
        assert config.theme == Theme.DARK

    def test_example_module_integration(self, temp_dir):
        """Test that examples work with the module."""
        from jsoncrack_for_sphinx.schema_finder import find_schema_for_object

        # Create example schema
        schema_data = {
            "type": "object",
            "properties": {"name": {"type": "string"}, "age": {"type": "integer"}},
        }

        schema_file = temp_dir / "User.create.schema.json"
        with open(schema_file, "w") as f:
            json.dump(schema_data, f)

        # Test finding schema
        result = find_schema_for_object("example.User.create", str(temp_dir))
        assert result is not None

        path, file_type = result
        assert Path(path).name == "User.create.schema.json"
        assert file_type == "schema"
