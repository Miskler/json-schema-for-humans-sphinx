"""
Tests for search pattern generation functionality.
"""

from jsoncrack_for_sphinx.config import PathSeparator, SearchPolicy
from jsoncrack_for_sphinx.patterns.pattern_generator import generate_search_patterns


class TestGenerateSearchPatterns:
    """Test search pattern generation functionality."""

    def test_generate_patterns_default_policy(self):
        """Test pattern generation with default policy."""
        policy = SearchPolicy()
        patterns = generate_search_patterns("mypackage.module.MyClass.method", policy)

        # Extract just the pattern names for comparison
        pattern_names = [pattern[0] for pattern in patterns]

        expected_patterns = [
            "MyClass.method.schema.json",
            "module.MyClass.method.schema.json",
            "method.schema.json",
            "mypackage.module.MyClass.method.schema.json",
        ]

        for expected in expected_patterns:
            assert expected in pattern_names

    def test_generate_patterns_with_package_name(self):
        """Test pattern generation including package name."""
        policy = SearchPolicy(include_package_name=True)
        patterns = generate_search_patterns("mypackage.module.MyClass.method", policy)

        # Extract pattern names
        pattern_names = [pattern[0] for pattern in patterns]

        # Should include full path patterns
        assert "mypackage.module.MyClass.method.schema.json" in pattern_names
        assert "MyClass.method.schema.json" in pattern_names

    def test_generate_patterns_slash_separator(self):
        """Test pattern generation with slash separators."""
        policy = SearchPolicy(
            include_package_name=True, path_to_file_separator=PathSeparator.SLASH
        )
        patterns = generate_search_patterns("mypackage.module.MyClass.method", policy)

        # Extract pattern names
        pattern_names = [pattern[0] for pattern in patterns]

        # Should use slashes for path separation
        assert "mypackage/module/MyClass.method.schema.json" in pattern_names

    def test_generate_patterns_no_separator(self):
        """Test pattern generation with no separators."""
        policy = SearchPolicy(
            path_to_file_separator=PathSeparator.NONE,
            path_to_class_separator=PathSeparator.NONE,
        )
        patterns = generate_search_patterns("mypackage.module.MyClass.method", policy)

        # Extract pattern names
        pattern_names = [pattern[0] for pattern in patterns]

        # Should concatenate without separators
        assert "MyClassmethod.schema.json" in pattern_names

    def test_generate_patterns_custom_patterns(self):
        """Test pattern generation with custom patterns."""
        custom_patterns = [
            "custom_{class_name}_{method_name}.json",
            "{object_name}_schema.json",
        ]
        policy = SearchPolicy(custom_patterns=custom_patterns)

        patterns = generate_search_patterns("mypackage.module.MyClass.method", policy)

        # Extract pattern names
        pattern_names = [pattern[0] for pattern in patterns]

        # Should include custom patterns
        assert "custom_MyClass_method.json" in pattern_names
        assert "mypackage.module.MyClass.method_schema.json" in pattern_names

    def test_generate_patterns_complex_object_name(self):
        """Test pattern generation with complex object names."""
        policy = SearchPolicy()
        patterns = generate_search_patterns(
            "perekrestok_api.endpoints.catalog.ProductService.similar", policy
        )

        # Extract pattern names
        pattern_names = [pattern[0] for pattern in patterns]

        expected_patterns = [
            "ProductService.similar.schema.json",
            "catalog.ProductService.similar.schema.json",
            "similar.schema.json",
            "perekrestok_api.endpoints.catalog.ProductService.similar.schema.json",
        ]

        for expected in expected_patterns:
            assert expected in pattern_names

    def test_generate_patterns_function_only(self):
        """Test pattern generation for standalone functions."""
        policy = SearchPolicy()
        patterns = generate_search_patterns("mypackage.utils.helper_function", policy)

        # Extract pattern names
        pattern_names = [pattern[0] for pattern in patterns]

        expected_patterns = [
            "helper_function.schema.json",
            "utils.helper_function.schema.json",
            "helper_function.schema.json",  # method name pattern same as function
            "mypackage.utils.helper_function.schema.json",
        ]

        for expected in expected_patterns:
            assert expected in pattern_names
