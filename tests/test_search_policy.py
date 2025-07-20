"""
Tests for schema search policy functionality.

This module tests the new configurable search policy feature that allows
flexible schema file naming conventions and search strategies.
"""

import json
import os
import tempfile
from pathlib import Path
from unittest.mock import Mock

import pytest

from jsoncrack_for_sphinx.config import (
    JsonCrackConfig,
    PathSeparator,
    SearchPolicy,
    parse_config,
)
from jsoncrack_for_sphinx.extension import (
    find_schema_for_object,
    generate_search_patterns,
)


class TestPathSeparator:
    """Test PathSeparator enum functionality."""

    def test_path_separator_values(self):
        """Test that PathSeparator enum has correct values."""
        assert PathSeparator.DOT.value == "."
        assert PathSeparator.SLASH.value == "/"
        assert PathSeparator.NONE.value == "none"

    def test_path_separator_string_representation(self):
        """Test string representation of PathSeparator."""
        assert str(PathSeparator.DOT) == "PathSeparator.DOT"
        assert str(PathSeparator.SLASH) == "PathSeparator.SLASH"
        assert str(PathSeparator.NONE) == "PathSeparator.NONE"


class TestSearchPolicy:
    """Test SearchPolicy class functionality."""

    def test_default_search_policy(self):
        """Test default SearchPolicy creation."""
        policy = SearchPolicy()
        
        assert policy.include_package_name is False
        assert policy.path_to_file_separator == PathSeparator.DOT
        assert policy.path_to_class_separator == PathSeparator.DOT
        assert policy.custom_patterns == []

    def test_custom_search_policy(self):
        """Test custom SearchPolicy creation."""
        custom_patterns = ["custom.{object_name}.json", "{class_name}_schema.json"]
        
        policy = SearchPolicy(
            include_package_name=True,
            path_to_file_separator=PathSeparator.SLASH,
            path_to_class_separator=PathSeparator.NONE,
            custom_patterns=custom_patterns
        )
        
        assert policy.include_package_name is True
        assert policy.path_to_file_separator == PathSeparator.SLASH
        assert policy.path_to_class_separator == PathSeparator.NONE
        assert policy.custom_patterns == custom_patterns

    def test_search_policy_representation(self):
        """Test SearchPolicy string representation."""
        policy = SearchPolicy(
            include_package_name=True,
            path_to_file_separator=PathSeparator.SLASH
        )
        
        repr_str = repr(policy)
        assert "SearchPolicy" in repr_str
        assert "include_package_name=True" in repr_str
        assert "path_to_file_separator=PathSeparator.SLASH" in repr_str


class TestGenerateSearchPatterns:
    """Test search pattern generation functionality."""

    def test_generate_patterns_default_policy(self):
        """Test pattern generation with default policy."""
        policy = SearchPolicy()
        patterns = generate_search_patterns(
            "mypackage.module.MyClass.method",
            policy
        )
        
        # Extract just the pattern names for comparison
        pattern_names = [pattern[0] for pattern in patterns]
        
        expected_patterns = [
            "MyClass.method.schema.json",
            "module.MyClass.method.schema.json",
            "method.schema.json",
            "mypackage.module.MyClass.method.schema.json"
        ]
        
        for expected in expected_patterns:
            assert expected in pattern_names

    def test_generate_patterns_with_package_name(self):
        """Test pattern generation including package name."""
        policy = SearchPolicy(include_package_name=True)
        patterns = generate_search_patterns(
            "mypackage.module.MyClass.method",
            policy
        )
        
        # Extract pattern names
        pattern_names = [pattern[0] for pattern in patterns]
        
        # Should include full path patterns
        assert "mypackage.module.MyClass.method.schema.json" in pattern_names
        assert "MyClass.method.schema.json" in pattern_names

    def test_generate_patterns_slash_separator(self):
        """Test pattern generation with slash separators."""
        policy = SearchPolicy(
            include_package_name=True,
            path_to_file_separator=PathSeparator.SLASH
        )
        patterns = generate_search_patterns(
            "mypackage.module.MyClass.method",
            policy
        )
        
        # Extract pattern names
        pattern_names = [pattern[0] for pattern in patterns]
        
        # Should use slashes for path separation
        assert "mypackage/module/MyClass.method.schema.json" in pattern_names

    def test_generate_patterns_no_separator(self):
        """Test pattern generation with no separators."""
        policy = SearchPolicy(
            path_to_file_separator=PathSeparator.NONE,
            path_to_class_separator=PathSeparator.NONE
        )
        patterns = generate_search_patterns(
            "mypackage.module.MyClass.method",
            policy
        )
        
        # Extract pattern names
        pattern_names = [pattern[0] for pattern in patterns]
        
        # Should concatenate without separators
        assert "MyClassmethod.schema.json" in pattern_names

    def test_generate_patterns_custom_patterns(self):
        """Test pattern generation with custom patterns."""
        custom_patterns = [
            "custom_{class_name}_{method_name}.json",
            "{object_name}_schema.json"
        ]
        policy = SearchPolicy(custom_patterns=custom_patterns)
        
        patterns = generate_search_patterns(
            "mypackage.module.MyClass.method",
            policy
        )
        
        # Extract pattern names
        pattern_names = [pattern[0] for pattern in patterns]
        
        # Should include custom patterns
        assert "custom_MyClass_method.json" in pattern_names
        assert "mypackage.module.MyClass.method_schema.json" in pattern_names

    def test_generate_patterns_complex_object_name(self):
        """Test pattern generation with complex object names."""
        policy = SearchPolicy()
        patterns = generate_search_patterns(
            "perekrestok_api.endpoints.catalog.ProductService.similar",
            policy
        )
        
        # Extract pattern names
        pattern_names = [pattern[0] for pattern in patterns]
        
        expected_patterns = [
            "ProductService.similar.schema.json",
            "catalog.ProductService.similar.schema.json", 
            "similar.schema.json",
            "perekrestok_api.endpoints.catalog.ProductService.similar.schema.json"
        ]
        
        for expected in expected_patterns:
            assert expected in pattern_names

    def test_generate_patterns_function_only(self):
        """Test pattern generation for standalone functions."""
        policy = SearchPolicy()
        patterns = generate_search_patterns(
            "mypackage.utils.helper_function",
            policy
        )
        
        # Extract pattern names
        pattern_names = [pattern[0] for pattern in patterns]
        
        expected_patterns = [
            "helper_function.schema.json",
            "utils.helper_function.schema.json",
            "helper_function.schema.json",  # method name pattern same as function
            "mypackage.utils.helper_function.schema.json"
        ]
        
        for expected in expected_patterns:
            assert expected in pattern_names


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
        with open(file_path, 'w') as f:
            json.dump(content, f)
        
        return str(file_path)

    def test_find_schema_default_policy(self):
        """Test schema finding with default policy."""
        # Create test schema file
        self.create_schema_file("MyClass.method.schema.json")
        
        policy = SearchPolicy()
        result = find_schema_for_object(
            "mypackage.module.MyClass.method",
            str(self.schema_dir),
            policy
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
        with open(schema_file, 'w') as f:
            json.dump({"type": "object"}, f)
        
        policy = SearchPolicy(
            include_package_name=True,
            path_to_file_separator=PathSeparator.SLASH
        )
        
        result = find_schema_for_object(
            "mypackage.module.MyClass.method",
            str(self.schema_dir),
            policy
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
            "mypackage.module.MyClass.method",
            str(self.schema_dir),
            policy
        )
        
        # Should find the highest priority one
        assert result is not None
        file_path, file_type = result
        assert str(file_path).endswith("MyClass.method.schema.json")

    def test_find_schema_not_found(self):
        """Test behavior when no schema is found."""
        policy = SearchPolicy()
        result = find_schema_for_object(
            "nonexistent.module.Class.method",
            str(self.schema_dir),
            policy
        )
        
        assert result is None

    def test_find_schema_no_directory(self):
        """Test behavior when schema directory doesn't exist."""
        policy = SearchPolicy()
        result = find_schema_for_object(
            "mypackage.module.MyClass.method",
            "/nonexistent/directory",
            policy
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
            "mypackage.module.MyClass.method",
            str(self.schema_dir),
            policy
        )
        
        assert result is not None
        file_path, file_type = result
        assert str(file_path).endswith("custom_MyClass_method.json")
        assert file_type == "json"

    def test_find_schema_target_case(self):
        """Test the specific case mentioned in the issue."""
        # Create the exact schema file from the issue
        self.create_schema_file("ProductService.similar.schema.json")
        
        policy = SearchPolicy()
        result = find_schema_for_object(
            "perekrestok_api.endpoints.catalog.ProductService.similar",
            str(self.schema_dir),
            policy
        )
        
        assert result is not None
        file_path, file_type = result
        assert str(file_path).endswith("ProductService.similar.schema.json")
        assert file_type == "schema"


class TestConfigIntegration:
    """Test integration with configuration system."""

    def test_parse_config_with_search_policy_dict(self):
        """Test parsing config with search policy as dictionary."""
        config_dict = {
            "search_policy": {
                "include_package_name": True,
                "path_to_file_separator": "/",
                "path_to_class_separator": ".",
                "custom_patterns": ["custom_{class_name}.json"]
            }
        }
        
        config = parse_config(config_dict)
        
        assert isinstance(config.search_policy, SearchPolicy)
        assert config.search_policy.include_package_name is True
        assert config.search_policy.path_to_file_separator == PathSeparator.SLASH
        assert config.search_policy.path_to_class_separator == PathSeparator.DOT
        assert config.search_policy.custom_patterns == ["custom_{class_name}.json"]

    def test_parse_config_with_search_policy_object(self):
        """Test parsing config with search policy as object."""
        policy = SearchPolicy(
            include_package_name=True,
            path_to_file_separator=PathSeparator.NONE
        )
        
        config_dict = {"search_policy": policy}
        config = parse_config(config_dict)
        
        assert config.search_policy is policy

    def test_parse_config_no_search_policy(self):
        """Test parsing config without search policy."""
        config_dict = {"theme": "dark"}
        config = parse_config(config_dict)
        
        assert isinstance(config.search_policy, SearchPolicy)
        # Should have default values
        assert config.search_policy.include_package_name is False
        assert config.search_policy.path_to_file_separator == PathSeparator.DOT

    def test_parse_config_invalid_separator_strings(self):
        """Test parsing with invalid separator strings."""
        config_dict = {
            "search_policy": {
                "path_to_file_separator": "invalid",
                "path_to_class_separator": "unknown"
            }
        }
        
        config = parse_config(config_dict)
        
        # Should fallback to DOT for invalid values
        assert config.search_policy.path_to_file_separator == PathSeparator.DOT
        assert config.search_policy.path_to_class_separator == PathSeparator.DOT

    def test_jsoncrack_config_with_search_policy(self):
        """Test JsonCrackConfig creation with search policy."""
        policy = SearchPolicy(include_package_name=True)
        config = JsonCrackConfig(search_policy=policy)
        
        assert config.search_policy is policy

    def test_jsoncrack_config_default_search_policy(self):
        """Test JsonCrackConfig creation with default search policy."""
        config = JsonCrackConfig()
        
        assert isinstance(config.search_policy, SearchPolicy)
        assert config.search_policy.include_package_name is False


class TestRegressionCases:
    """Test cases for regression prevention."""

    def test_backwards_compatibility(self):
        """Test that existing functionality still works."""
        # This should work exactly as before
        policy = SearchPolicy()  # Default policy
        patterns = generate_search_patterns("module.Class.method", policy)
        
        # Extract pattern names
        pattern_names = [pattern[0] for pattern in patterns]
        
        # Should still generate basic patterns
        assert "Class.method.schema.json" in pattern_names
        assert "method.schema.json" in pattern_names

    def test_mock_object_handling(self):
        """Test that Mock objects are handled correctly in parse_config."""
        mock_config = Mock()
        
        # Should not raise an exception
        config = parse_config(mock_config)
        
        assert isinstance(config, JsonCrackConfig)
        assert isinstance(config.search_policy, SearchPolicy)

    def test_empty_object_name(self):
        """Test handling of edge cases with empty or invalid object names."""
        policy = SearchPolicy()
        
        # Empty string
        patterns = generate_search_patterns("", policy)
        assert len(patterns) > 0  # Should handle gracefully
        
        # Single component
        patterns = generate_search_patterns("function", policy)
        pattern_names = [pattern[0] for pattern in patterns]
        assert "function.schema.json" in pattern_names

    def test_complex_nested_object_names(self):
        """Test handling of deeply nested object names."""
        policy = SearchPolicy()
        complex_name = "very.deep.nested.package.module.submodule.Class.SubClass.method"
        
        patterns = generate_search_patterns(complex_name, policy)
        pattern_names = [pattern[0] for pattern in patterns]
        
        # Should handle gracefully and generate reasonable patterns
        assert "SubClass.method.schema.json" in pattern_names
        assert "method.schema.json" in pattern_names
        assert len(patterns) > 0
