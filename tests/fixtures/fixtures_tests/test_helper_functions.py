"""
Tests for helper functions for creating test schemas.
"""

import json

from jsoncrack_for_sphinx.utils.fixtures import (
    create_function_schema,
    create_method_schema,
    create_option_schema,
)


class TestHelperFunctions:
    """Test helper functions for creating test schemas."""

    def test_create_method_schema(self, temp_dir):
        """Test creating a method schema file."""
        schema_data = {
            "type": "object",
            "title": "Method Schema",
            "properties": {"param1": {"type": "string"}, "param2": {"type": "integer"}},
        }

        schema_path = create_method_schema(
            temp_dir, "TestClass", "test_method", schema_data
        )

        assert schema_path.name == "TestClass.test_method.schema.json"
        assert schema_path.exists()

        # Verify content
        with open(schema_path) as f:
            loaded_data = json.load(f)

        assert loaded_data == schema_data
        assert loaded_data["title"] == "Method Schema"

    def test_create_function_schema(self, temp_dir):
        """Test creating a function schema file."""
        schema_data = {
            "type": "object",
            "title": "Function Schema",
            "properties": {"input": {"type": "array"}, "options": {"type": "object"}},
        }

        schema_path = create_function_schema(temp_dir, "test_function", schema_data)

        assert schema_path.name == "test_function.schema.json"
        assert schema_path.exists()

        # Verify content
        with open(schema_path) as f:
            loaded_data = json.load(f)

        assert loaded_data == schema_data
        assert loaded_data["title"] == "Function Schema"

    def test_create_option_schema(self, temp_dir):
        """Test creating an option schema file."""
        schema_data = {
            "type": "object",
            "title": "Option Schema",
            "properties": {
                "advanced": {"type": "boolean"},
                "config": {"type": "object"},
            },
        }

        schema_path = create_option_schema(
            temp_dir, "base_function", "advanced", schema_data
        )

        assert schema_path.name == "base_function.advanced.schema.json"
        assert schema_path.exists()

        # Verify content
        with open(schema_path) as f:
            loaded_data = json.load(f)

        assert loaded_data == schema_data
        assert loaded_data["title"] == "Option Schema"

    def test_create_method_schema_with_options(self, temp_dir):
        """Test creating a method schema with options."""
        schema_data = {
            "type": "object",
            "title": "Method Option Schema",
            "properties": {
                "advanced_param": {"type": "string"},
                "debug": {"type": "boolean"},
            },
        }

        schema_path = create_option_schema(
            temp_dir, "TestClass.method", "advanced", schema_data
        )

        assert schema_path.name == "TestClass.method.advanced.schema.json"
        assert schema_path.exists()

        # Verify content
        with open(schema_path) as f:
            loaded_data = json.load(f)

        assert loaded_data == schema_data
