"""
Tests for pytest fixtures functionality.
"""

import json


class TestFixtures:
    """Test pytest fixtures."""

    def test_schema_to_rst_fixture_function(self, schema_to_rst_fixture, schema_file):
        """Test that schema_to_rst_fixture returns the correct function."""
        # The fixture should return the schema_to_rst function
        from jsoncrack_for_sphinx.generators.rst_generator import schema_to_rst

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
