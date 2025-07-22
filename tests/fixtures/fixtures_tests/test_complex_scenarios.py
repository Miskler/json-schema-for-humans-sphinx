"""
Tests for complex scenarios with helper functions.
"""

import json

from jsoncrack_for_sphinx.utils.fixtures import (
    create_function_schema,
    create_method_schema,
    create_option_schema,
)


class TestComplexScenarios:
    """Test complex scenarios with helper functions."""

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
