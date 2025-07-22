"""
Tests for schema finding functionality.
"""

import json
from pathlib import Path

from jsoncrack_for_sphinx.schema.schema_finder import find_schema_for_object


class TestFindSchemaForObject:
    """Test finding schema files for objects."""

    def test_find_schema_for_method(self, schema_dir):
        """Test finding schema for a method."""
        result = find_schema_for_object("example_module.User.create", str(schema_dir))

        assert result is not None
        schema_path, file_type = result
        assert Path(schema_path).name == "User.create.schema.json"
        assert file_type == "schema"

    def test_find_schema_for_function(self, schema_dir):
        """Test finding schema for a function."""
        result = find_schema_for_object("example_module.process_data", str(schema_dir))

        assert result is not None
        schema_path, file_type = result
        assert Path(schema_path).name == "process_data.schema.json"
        assert file_type == "schema"

    def test_find_json_for_method(self, schema_dir):
        """Test finding JSON data for a method."""
        result = find_schema_for_object("example_module.User.example", str(schema_dir))

        assert result is not None
        schema_path, file_type = result
        assert Path(schema_path).name == "User.example.json"
        assert file_type == "json"

    def test_find_schema_not_found(self, schema_dir):
        """Test finding schema for non-existent object."""
        result = find_schema_for_object(
            "example_module.NonExistent.method", str(schema_dir)
        )
        assert result is None

    def test_find_schema_no_schema_dir(self):
        """Test finding schema when no schema directory is configured."""
        result = find_schema_for_object("example_module.User.create", None)
        assert result is None

    def test_find_schema_non_existent_dir(self):
        """Test finding schema in non-existent directory."""
        result = find_schema_for_object(
            "example_module.User.create", "/non/existent/dir"
        )
        assert result is None

    def test_find_schema_priority_schema_over_json(self, temp_dir):
        """Test that .schema.json files have priority over .json files."""
        # Create both schema and json files
        schema_data = {"type": "object", "title": "Schema File"}
        json_data = {"example": "data"}

        schema_path = temp_dir / "User.method.schema.json"
        with open(schema_path, "w") as f:
            json.dump(schema_data, f)

        json_path = temp_dir / "User.method.json"
        with open(json_path, "w") as f:
            json.dump(json_data, f)

        result = find_schema_for_object("example_module.User.method", str(temp_dir))

        assert result is not None
        found_path, file_type = result
        assert Path(found_path).name == "User.method.schema.json"
        assert file_type == "schema"
