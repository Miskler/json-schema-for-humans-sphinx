"""
Tests for configuration integration and regression cases.
"""

import json
import tempfile
from pathlib import Path
from unittest.mock import Mock

from jsoncrack_for_sphinx.config import (
    JsonCrackConfig,
    PathSeparator,
    SearchPolicy,
    parse_config,
)
from jsoncrack_for_sphinx.patterns.pattern_generator import generate_search_patterns
from jsoncrack_for_sphinx.schema.schema_finder import find_schema_for_object


class TestConfigIntegration:
    """Test integration with configuration system."""

    def test_parse_config_with_search_policy_dict(self):
        """Test parsing config with search policy as dictionary."""
        config_dict = {
            "search_policy": {
                "include_package_name": True,
                "path_to_file_separator": "/",
                "path_to_class_separator": ".",
                "custom_patterns": ["custom_{class_name}.json"],
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
            include_package_name=True, path_to_file_separator=PathSeparator.NONE
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
                "path_to_class_separator": "unknown",
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


class TestTargetCases:
    """Test specific target cases from issues."""

    def setup_method(self):
        """Set up test directory."""
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

    def test_find_schema_target_case(self):
        """Test the specific case mentioned in the issue."""
        # Create the exact schema file from the issue
        self.create_schema_file("ProductService.similar.schema.json")

        policy = SearchPolicy()
        result = find_schema_for_object(
            "perekrestok_api.endpoints.catalog.ProductService.similar",
            str(self.schema_dir),
            policy,
        )

        assert result is not None
        file_path, file_type = result
        assert str(file_path).endswith("ProductService.similar.schema.json")
        assert file_type == "schema"
