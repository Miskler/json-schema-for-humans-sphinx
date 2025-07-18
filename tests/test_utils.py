"""
Tests for the utils module.
"""

import json
from pathlib import Path

import pytest

from jsoncrack_for_sphinx.utils import (
    create_schema_index,
    find_schema_files,
    get_schema_info,
    schema_to_rst,
    validate_schema_file,
)


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

        # The actual implementation raises RuntimeError when the schema processing fails
        with pytest.raises(RuntimeError, match="Error processing schema file"):
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


class TestValidateSchemaFile:
    """Test schema file validation."""

    def test_validate_valid_schema(self, schema_file):
        """Test validation of valid schema file."""
        assert validate_schema_file(schema_file) is True

    def test_validate_invalid_json(self, temp_dir):
        """Test validation of invalid JSON file."""
        invalid_file = temp_dir / "invalid.json"
        with open(invalid_file, "w") as f:
            f.write("invalid json content")

        assert validate_schema_file(invalid_file) is False

    def test_validate_non_existent_file(self, temp_dir):
        """Test validation of non-existent file."""
        non_existent_file = temp_dir / "non_existent.json"
        assert validate_schema_file(non_existent_file) is False

    def test_validate_empty_file(self, temp_dir):
        """Test validation of empty file."""
        empty_file = temp_dir / "empty.json"
        empty_file.touch()
        assert validate_schema_file(empty_file) is False

    def test_validate_valid_json_data(self, json_file):
        """Test validation of valid JSON data file."""
        assert validate_schema_file(json_file) is True


class TestFindSchemaFiles:
    """Test finding schema files."""

    def test_find_schema_files_default_pattern(self, schema_dir):
        """Test finding schema files with default pattern."""
        files = find_schema_files(schema_dir)

        schema_files = [f.name for f in files]
        assert "User.create.schema.json" in schema_files
        assert "User.update.schema.json" in schema_files
        assert "process_data.schema.json" in schema_files
        # Should not include .json files
        assert "User.example.json" not in schema_files

    def test_find_schema_files_custom_pattern(self, schema_dir):
        """Test finding schema files with custom pattern."""
        files = find_schema_files(schema_dir, pattern="*.json")

        json_files = [f.name for f in files]
        assert "User.example.json" in json_files
        assert "User.create.schema.json" in json_files
        assert "User.update.schema.json" in json_files
        assert "process_data.schema.json" in json_files
        assert "invalid.schema.json" in json_files

    def test_find_schema_files_specific_pattern(self, schema_dir):
        """Test finding schema files with specific pattern."""
        files = find_schema_files(schema_dir, pattern="User.*.schema.json")

        user_files = [f.name for f in files]
        assert "User.create.schema.json" in user_files
        assert "User.update.schema.json" in user_files
        assert "process_data.schema.json" not in user_files

    def test_find_schema_files_empty_directory(self, temp_dir):
        """Test finding schema files in empty directory."""
        files = find_schema_files(temp_dir)
        assert len(files) == 0

    def test_find_schema_files_non_existent_directory(self):
        """Test finding schema files in non-existent directory."""
        non_existent_dir = Path("/non/existent/directory")
        files = find_schema_files(non_existent_dir)
        assert len(files) == 0


class TestGetSchemaInfo:
    """Test getting schema information."""

    def test_get_schema_info_complete(self, schema_file, sample_schema):
        """Test getting info from complete schema."""
        info = get_schema_info(schema_file)

        assert info["file_name"] == "User.schema.json"
        assert info["title"] == sample_schema["title"]
        assert info["description"] == sample_schema["description"]
        assert info["type"] == sample_schema["type"]
        assert set(info["properties"]) == set(sample_schema["properties"].keys())
        assert info["required"] == sample_schema["required"]

    def test_get_schema_info_minimal(self, temp_dir):
        """Test getting info from minimal schema."""
        minimal_schema = {"type": "string"}

        schema_file = temp_dir / "minimal.schema.json"
        with open(schema_file, "w") as f:
            json.dump(minimal_schema, f)

        info = get_schema_info(schema_file)

        assert info["file_name"] == "minimal.schema.json"
        assert info["title"] == ""
        assert info["description"] == ""
        assert info["type"] == "string"
        assert info["properties"] == []
        assert info["required"] == []

    def test_get_schema_info_non_existent_file(self, temp_dir):
        """Test getting info from non-existent file."""
        non_existent_file = temp_dir / "non_existent.schema.json"

        with pytest.raises(FileNotFoundError):
            get_schema_info(non_existent_file)

    def test_get_schema_info_invalid_json(self, temp_dir):
        """Test getting info from invalid JSON file."""
        invalid_file = temp_dir / "invalid.schema.json"
        with open(invalid_file, "w") as f:
            f.write("invalid json content")

        with pytest.raises(ValueError, match="Invalid JSON"):
            get_schema_info(invalid_file)

    def test_get_schema_info_complex_schema(self, temp_dir):
        """Test getting info from complex schema."""
        complex_schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "title": "Complex Object",
            "description": "A complex object with nested properties",
            "properties": {
                "id": {"type": "integer"},
                "profile": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "age": {"type": "integer"},
                    },
                },
                "tags": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["id", "profile"],
        }

        schema_file = temp_dir / "complex.schema.json"
        with open(schema_file, "w") as f:
            json.dump(complex_schema, f)

        info = get_schema_info(schema_file)

        assert info["title"] == "Complex Object"
        assert info["description"] == "A complex object with nested properties"
        assert set(info["properties"]) == {"id", "profile", "tags"}
        assert info["required"] == ["id", "profile"]


class TestCreateSchemaIndex:
    """Test creating schema index."""

    def test_create_schema_index_with_files(self, schema_dir):
        """Test creating index with schema files."""
        index = create_schema_index(schema_dir)

        assert "Schema Index" in index
        assert "=" * len("Schema Index") in index
        assert "User.create.schema.json" in index
        assert "User.update.schema.json" in index
        assert "process_data.schema.json" in index
        assert ":Title:" in index
        assert ":Type:" in index
        assert ":Properties:" in index

    def test_create_schema_index_empty_directory(self, temp_dir):
        """Test creating index with empty directory."""
        index = create_schema_index(temp_dir)
        assert "No schema files found." in index

    def test_create_schema_index_with_invalid_file(self, temp_dir):
        """Test creating index with invalid schema file."""
        # Create a valid schema file
        valid_schema = {
            "type": "object",
            "title": "Valid Schema",
            "properties": {"name": {"type": "string"}},
        }

        valid_file = temp_dir / "valid.schema.json"
        with open(valid_file, "w") as f:
            json.dump(valid_schema, f)

        # Create an invalid schema file
        invalid_file = temp_dir / "invalid.schema.json"
        with open(invalid_file, "w") as f:
            f.write("invalid json content")

        index = create_schema_index(temp_dir)

        # Should contain valid file info
        assert "valid.schema.json" in index
        assert "Valid Schema" in index

        # Should contain error info for invalid file
        assert "invalid.schema.json" in index
        assert "Error:" in index

    def test_create_schema_index_sorting(self, temp_dir):
        """Test that schema index is sorted by filename."""
        schemas = {
            "z_last.schema.json": {"type": "string", "title": "Last"},
            "a_first.schema.json": {"type": "string", "title": "First"},
            "m_middle.schema.json": {"type": "string", "title": "Middle"},
        }

        for filename, content in schemas.items():
            file_path = temp_dir / filename
            with open(file_path, "w") as f:
                json.dump(content, f)

        index = create_schema_index(temp_dir)

        # Extract filenames in order they appear in index
        lines = index.split("\n")
        file_lines = [
            line for line in lines if line.startswith("**") and line.endswith("**")
        ]

        assert "**a_first.schema.json**" in file_lines[0]
        assert "**m_middle.schema.json**" in file_lines[1]
        assert "**z_last.schema.json**" in file_lines[2]
