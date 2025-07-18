"""
Tests for the fixtures module.
"""

import json

from jsoncrack_for_sphinx.fixtures import (
    create_function_schema,
    create_method_schema,
    create_option_schema,
)


class TestFixtures:
    """Test pytest fixtures."""

    def test_schema_to_rst_fixture_function(self, schema_to_rst_fixture, schema_file):
        """Test that schema_to_rst_fixture returns the correct function."""
        # The fixture should return the schema_to_rst function
        from jsoncrack_for_sphinx.utils import schema_to_rst

        assert schema_to_rst_fixture == schema_to_rst

        # Test that the function works
        result = schema_to_rst_fixture(schema_file, title="Test")
        assert "Test" in result
        assert ".. raw:: html" in result

    def test_schema_to_rst_fixture_usage(self, schema_to_rst_fixture, temp_dir):
        """Test using schema_to_rst_fixture in a test scenario."""
        # Create a test schema
        test_schema = {
            "type": "object",
            "title": "Test Schema",
            "properties": {"name": {"type": "string"}},
        }

        schema_path = temp_dir / "test.schema.json"
        with open(schema_path, "w") as f:
            json.dump(test_schema, f)

        # Use the fixture
        result = schema_to_rst_fixture(schema_path, title="Fixture Test")

        assert "Fixture Test" in result
        assert "=" * len("Fixture Test") in result
        assert ".. raw:: html" in result
        assert "json-schema-container" in result


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

    def test_helper_functions_with_complex_data(self, temp_dir):
        """Test helper functions with complex schema data."""
        complex_schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "title": "Complex Schema",
            "description": "A complex schema with nested objects and arrays",
            "properties": {
                "user": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "profile": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "contacts": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "type": {"type": "string"},
                                            "value": {"type": "string"},
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
                "metadata": {"type": "object", "additionalProperties": True},
            },
            "required": ["user"],
        }

        # Test with method schema
        method_path = create_method_schema(
            temp_dir, "ComplexClass", "process", complex_schema
        )
        assert method_path.exists()

        # Test with function schema
        function_path = create_function_schema(
            temp_dir, "process_complex", complex_schema
        )
        assert function_path.exists()

        # Test with option schema
        option_path = create_option_schema(
            temp_dir, "complex_base", "detailed", complex_schema
        )
        assert option_path.exists()

        # Verify all files have the same content
        for path in [method_path, function_path, option_path]:
            with open(path) as f:
                loaded_data = json.load(f)
            assert loaded_data == complex_schema

    def test_helper_functions_file_overwrite(self, temp_dir):
        """Test that helper functions overwrite existing files."""
        schema_data_v1 = {"type": "string", "title": "Version 1"}

        schema_data_v2 = {"type": "integer", "title": "Version 2"}

        # Create first version
        schema_path = create_function_schema(temp_dir, "test_func", schema_data_v1)

        with open(schema_path) as f:
            loaded_data = json.load(f)
        assert loaded_data["title"] == "Version 1"

        # Create second version (should overwrite)
        schema_path = create_function_schema(temp_dir, "test_func", schema_data_v2)

        with open(schema_path) as f:
            loaded_data = json.load(f)
        assert loaded_data["title"] == "Version 2"
        assert loaded_data["type"] == "integer"
