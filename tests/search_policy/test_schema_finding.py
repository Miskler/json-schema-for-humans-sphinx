"""
Tests for schema file finding functionality.
"""

import json
import tempfile
from pathlib import Path

from jsoncrack_for_sphinx.config import PathSeparator, SearchPolicy
from jsoncrack_for_sphinx.schema.schema_finder import find_schema_for_object


class TestFindSchemaForObject:
    """Test schema file finding functionality."""

    def setup_method(self):
        """Set up test directory with schema files."""
        self.temp_dir = tempfile.mkdtemp()
        self.schema_dir = Path(self.temp_dir) / "schemas"
        self.schema_dir.mkdir()

    def teardown_method(self):
        """Clean up test directory."""
        import shutil

        shutil.rmtree(self.temp_dir)

    def create_schema_file(self, filename: str, content: dict = None):
        """Create a schema file with given content."""
        if content is None:
            content = {"type": "object", "properties": {"test": {"type": "string"}}}

        file_path = self.schema_dir / filename
        with open(file_path, "w") as f:
            json.dump(content, f)

        return str(file_path)

    def test_find_schema_default_policy(self):
        """Test schema finding with default policy."""
        # Create test schema file
        self.create_schema_file("MyClass.method.schema.json")

        policy = SearchPolicy()
        result = find_schema_for_object(
            "mypackage.module.MyClass.method", str(self.schema_dir), policy
        )

        assert result is not None
        file_path, file_type = result
        assert str(file_path).endswith("MyClass.method.schema.json")
        assert file_type == "schema"

    def test_find_schema_with_package_path(self):
        """Test schema finding with package path structure."""
        # Create directory structure
        package_dir = self.schema_dir / "mypackage" / "module"
        package_dir.mkdir(parents=True)

        schema_file = package_dir / "MyClass.method.schema.json"
        with open(schema_file, "w") as f:
            json.dump({"type": "object"}, f)

        policy = SearchPolicy(
            include_package_name=True, path_to_file_separator=PathSeparator.SLASH
        )

        result = find_schema_for_object(
            "mypackage.module.MyClass.method", str(self.schema_dir), policy
        )

        assert result is not None
        file_path, file_type = result
        assert "mypackage/module/MyClass.method.schema.json" in str(file_path)

    def test_find_schema_priority_order(self):
        """Test that schemas are found in correct priority order."""
        # Create multiple schema files
        self.create_schema_file("MyClass.method.schema.json")  # Highest priority
        self.create_schema_file("module.MyClass.method.schema.json")
        self.create_schema_file("method.schema.json")

        policy = SearchPolicy()
        result = find_schema_for_object(
            "mypackage.module.MyClass.method", str(self.schema_dir), policy
        )

        # Should find the highest priority one
        assert result is not None
        file_path, file_type = result
        assert str(file_path).endswith("MyClass.method.schema.json")

    def test_find_schema_not_found(self):
        """Test behavior when no schema is found."""
        policy = SearchPolicy()
        result = find_schema_for_object(
            "nonexistent.module.Class.method", str(self.schema_dir), policy
        )

        assert result is None

    def test_find_schema_no_directory(self):
        """Test behavior when schema directory doesn't exist."""
        policy = SearchPolicy()
        result = find_schema_for_object(
            "mypackage.module.MyClass.method", "/nonexistent/directory", policy
        )

        assert result is None

    def test_find_schema_custom_patterns(self):
        """Test schema finding with custom patterns."""
        # Create schema file matching custom pattern
        self.create_schema_file("custom_MyClass_method.json")

        policy = SearchPolicy(
            custom_patterns=["custom_{class_name}_{method_name}.json"]
        )

        result = find_schema_for_object(
            "mypackage.module.MyClass.method", str(self.schema_dir), policy
        )

        assert result is not None
        file_path, file_type = result
        assert str(file_path).endswith("custom_MyClass_method.json")
        assert file_type == "json"
