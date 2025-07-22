"""
Tests for schema file finding and information extraction.
"""

import json
from pathlib import Path

from jsoncrack_for_sphinx.schema.schema_utils import find_schema_files, get_schema_info


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

    def test_get_schema_info_invalid_file(self, temp_dir):
        """Test getting info from invalid file."""
        invalid_file = temp_dir / "invalid.schema.json"
        with open(invalid_file, "w") as f:
            f.write("invalid json")

        info = get_schema_info(invalid_file)

        assert info["file_name"] == "invalid.schema.json"
        assert info["title"] == ""
        assert info["description"] == ""
        assert info["type"] == ""
        assert info["properties"] == []
        assert info["required"] == []
