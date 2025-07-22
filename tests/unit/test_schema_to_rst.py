"""
Tests for schema to RST conversion functionality.
"""

import json

import pytest

from jsoncrack_for_sphinx.generators.rst_generator import schema_to_rst


class TestSchemaToRst:
    """Test schema to RST conversion."""

    def test_schema_to_rst_with_title(self, schema_file):
        """Test converting schema to RST with title."""
        result = schema_to_rst(schema_file, title="Test Schema")

        assert "Test Schema" in result
        assert "=" * len("Test Schema") in result
        assert ".. raw:: html" in result
        assert "json-schema-container" in result

    def test_schema_to_rst_without_title(self, schema_file):
        """Test converting schema to RST without title."""
        result = schema_to_rst(schema_file)

        assert ".. raw:: html" in result
        assert "json-schema-container" in result
        # Should not contain title section
        assert "=" not in result.split(".. raw:: html")[0]

    def test_schema_to_rst_file_not_found(self, temp_dir):
        """Test schema to RST with non-existent file."""
        non_existent_file = temp_dir / "non_existent.schema.json"

        with pytest.raises(FileNotFoundError):
            schema_to_rst(non_existent_file)

    def test_schema_to_rst_invalid_json(self, temp_dir):
        """Test schema to RST with invalid JSON."""
        invalid_file = temp_dir / "invalid.schema.json"
        with open(invalid_file, "w") as f:
            f.write("invalid json content")

        # The implementation raises ValueError when JSON parsing fails
        with pytest.raises(ValueError, match="Invalid JSON in schema file"):
            schema_to_rst(invalid_file)

    def test_schema_to_rst_complex_schema(self, temp_dir):
        """Test schema to RST with complex schema."""
        complex_schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "title": "Complex Schema",
            "description": "A complex schema with nested objects",
            "properties": {
                "user": {
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
                }
            },
        }

        schema_file = temp_dir / "complex.schema.json"
        with open(schema_file, "w") as f:
            json.dump(complex_schema, f)

        result = schema_to_rst(schema_file, title="Complex Test")

        assert "Complex Test" in result
        assert ".. raw:: html" in result
