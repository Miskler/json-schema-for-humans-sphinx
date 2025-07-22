"""
Performance and stress tests for the jsoncrack-for-sphinx extension.
"""

import json
import time
from unittest.mock import Mock

from jsoncrack_for_sphinx.core.autodoc import autodoc_process_signature
from jsoncrack_for_sphinx.generators.html_generator import generate_schema_html
from jsoncrack_for_sphinx.schema.schema_finder import find_schema_for_object
from jsoncrack_for_sphinx.schema.schema_utils import (
    find_schema_files,
    validate_schema_file,
)


class TestPerformance:
    """Performance tests for the extension."""

    def test_find_schema_for_object_performance(self, temp_dir):
        """Test performance of finding schema for object."""
        # Create many schema files
        num_files = 50
        for i in range(num_files):
            schema_data = {
                "type": "object",
                "title": f"Schema {i}",
                "properties": {"prop": {"type": "string"}},
            }

            with open(temp_dir / f"schema_{i}.schema.json", "w") as f:
                json.dump(schema_data, f)

        # Test performance
        start_time = time.time()

        # Find existing schema
        result = find_schema_for_object("module.schema_25", str(temp_dir))

        end_time = time.time()

        # Should be reasonably fast
        assert end_time - start_time < 1.0
        assert result is not None

    def test_generate_schema_html_performance(self, temp_dir):
        """Test performance of HTML generation."""
        # Create complex schema
        schema_data = {
            "type": "object",
            "properties": {
                f"prop_{i}": {
                    "type": "object",
                    "properties": {f"nested_{j}": {"type": "string"} for j in range(5)},
                }
                for i in range(10)
            },
        }

        schema_file = temp_dir / "complex.schema.json"
        with open(schema_file, "w") as f:
            json.dump(schema_data, f)

        # Test performance
        start_time = time.time()

        html = generate_schema_html(schema_file, "schema")

        end_time = time.time()

        # Should be reasonably fast
        assert end_time - start_time < 2.0
        assert "jsoncrack-container" in html

    def test_autodoc_processing_performance(self, temp_dir):
        """Test performance of autodoc processing."""
        # Create schema files
        for i in range(20):
            schema_data = {"type": "object", "title": f"Test {i}"}
            with open(temp_dir / f"test_{i}.schema.json", "w") as f:
                json.dump(schema_data, f)

        # Mock Sphinx app
        mock_app = Mock()
        mock_app.config = Mock()
        mock_app.config.json_schema_dir = str(temp_dir)
        mock_app.env = Mock()
        mock_app.env._jsoncrack_schema_paths = {}

        # Test performance of signature processing
        start_time = time.time()

        for i in range(20):
            autodoc_process_signature(
                mock_app,
                "function",
                f"module.test_{i}",
                Mock(),
                {},
                "signature",
                "return_annotation",
            )

        end_time = time.time()

        # Should complete within reasonable time
        assert end_time - start_time < 1.0, "Autodoc processing should be fast"


class TestStress:
    """Stress tests for edge cases."""

    def test_large_schema_stress(self, temp_dir):
        """Test handling of large schemas."""
        # Create very large schema
        schema_data = {
            "type": "object",
            "properties": {
                f"property_{i}": {
                    "type": "string",
                    "description": f"Property {i} description",
                }
                for i in range(100)
            },
        }

        schema_file = temp_dir / "large.schema.json"
        with open(schema_file, "w") as f:
            json.dump(schema_data, f)

        # Should handle large schema without crashing
        assert validate_schema_file(schema_file) is True

        html = generate_schema_html(schema_file, "schema")
        assert "jsoncrack-container" in html

    def test_many_files_stress(self, temp_dir):
        """Test handling of many schema files."""
        # Create many files
        num_files = 100
        for i in range(num_files):
            schema_data = {"type": "string", "title": f"Schema {i}"}
            with open(temp_dir / f"file_{i}.schema.json", "w") as f:
                json.dump(schema_data, f)

        # Should handle many files efficiently
        start_time = time.time()
        files = find_schema_files(temp_dir)
        end_time = time.time()

        assert len(files) == num_files
        assert end_time - start_time < 1.0  # Should be fast

    def test_malformed_json_handling(self, temp_dir):
        """Test handling of malformed JSON."""
        # Create malformed JSON file
        malformed_file = temp_dir / "malformed.schema.json"
        with open(malformed_file, "w") as f:
            f.write("invalid json content")

        # Should handle gracefully
        assert validate_schema_file(malformed_file) is False

        html = generate_schema_html(malformed_file, "schema")
        assert "error" in html.lower()
