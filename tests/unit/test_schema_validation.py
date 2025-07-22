"""
Tests for schema file validation functionality.
"""

from jsoncrack_for_sphinx.schema.schema_utils import validate_schema_file


class TestValidateSchemaFile:
    """Test schema file validation."""

    def test_validate_valid_schema(self, schema_file):
        """Test validation of valid schema file."""
        assert validate_schema_file(schema_file) is True

    def test_validate_invalid_json(self, temp_dir):
        """Test validation of invalid JSON file."""
        invalid_file = temp_dir / "invalid.schema.json"
        with open(invalid_file, "w") as f:
            f.write("invalid json content")

        assert validate_schema_file(invalid_file) is False

    def test_validate_non_existent_file(self, temp_dir):
        """Test validation of non-existent file."""
        non_existent_file = temp_dir / "non_existent.schema.json"
        assert validate_schema_file(non_existent_file) is False

    def test_validate_empty_file(self, temp_dir):
        """Test validation of empty file."""
        empty_file = temp_dir / "empty.schema.json"
        empty_file.touch()
        assert validate_schema_file(empty_file) is False

    def test_validate_valid_json_data(self, json_file):
        """Test validation of valid JSON data file."""
        assert validate_schema_file(json_file) is True
