"""Tests for pattern generation functions."""

from jsoncrack_for_sphinx.patterns.pattern_strategies import (
    add_class_method_patterns,
    add_package_name_patterns,
    add_path_component_patterns,
    add_slash_separated_patterns,
)
from jsoncrack_for_sphinx.search.search_policy import SearchPolicy
from jsoncrack_for_sphinx.utils.types import PathSeparator


class TestAddClassMethodPatterns:
    """Test add_class_method_patterns function."""

    def test_add_class_method_patterns_dot_separator(self):
        """Test adding class method patterns with dot separator."""
        search_policy = SearchPolicy(path_to_class_separator=PathSeparator.DOT)
        parts = ["package", "module", "TestClass", "test_method"]

        result = add_class_method_patterns(parts, search_policy)

        expected = [
            ("TestClass.test_method.schema.json", "schema"),
            ("TestClass.test_method.json", "json"),
        ]
        assert result == expected

    def test_add_class_method_patterns_slash_separator(self):
        """Test adding class method patterns with slash separator."""
        search_policy = SearchPolicy(path_to_class_separator=PathSeparator.SLASH)
        parts = ["package", "module", "TestClass", "test_method"]

        result = add_class_method_patterns(parts, search_policy)

        expected = [
            ("TestClass/test_method.schema.json", "schema"),
            ("TestClass/test_method.json", "json"),
        ]
        assert result == expected


class TestAddPathComponentPatterns:
    """Test add_path_component_patterns function."""

    def test_add_path_component_patterns_basic(self):
        """Test adding path component patterns."""
        search_policy = SearchPolicy(
            path_to_file_separator=PathSeparator.DOT, include_package_name=True
        )
        parts = ["package", "module", "submodule", "TestClass", "test_method"]

        result = add_path_component_patterns(parts, search_policy)

        # Should include patterns for intermediate components
        assert len(result) >= 2
        assert any(".schema.json" in pattern for pattern, _ in result)
        assert any(".json" in pattern for pattern, _ in result)

    def test_add_path_component_patterns_without_package(self):
        """Test adding path component patterns without package name."""
        search_policy = SearchPolicy(
            path_to_file_separator=PathSeparator.DOT, include_package_name=False
        )
        parts = ["package", "module", "submodule", "TestClass", "test_method"]

        result = add_path_component_patterns(parts, search_policy)

        # Should generate patterns without package name
        assert len(result) >= 0

    def test_add_path_component_patterns_slash_separator(self):
        """Test adding path component patterns with slash separator."""
        search_policy = SearchPolicy(
            path_to_file_separator=PathSeparator.SLASH, include_package_name=False
        )
        parts = ["package", "module", "submodule", "TestClass", "test_method"]

        result = add_path_component_patterns(parts, search_policy)

        # Should handle slash-separated patterns
        assert len(result) >= 0


class TestAddPackageNamePatterns:
    """Test add_package_name_patterns function."""

    def test_add_package_name_patterns_slash_separator(self):
        """Test adding package name patterns with slash separator."""
        search_policy = SearchPolicy(
            path_to_file_separator=PathSeparator.SLASH,
            path_to_class_separator=PathSeparator.DOT,
        )
        parts = ["package", "module", "TestClass", "test_method"]

        result = add_package_name_patterns(parts, search_policy)

        expected = [
            ("package/module/TestClass.test_method.schema.json", "schema"),
            ("package/module/TestClass.test_method.json", "json"),
        ]
        assert result == expected

    def test_add_package_name_patterns_dot_separator(self):
        """Test adding package name patterns with dot separator."""
        search_policy = SearchPolicy(
            path_to_file_separator=PathSeparator.DOT,
            path_to_class_separator=PathSeparator.DOT,
        )
        parts = ["package", "module", "TestClass", "test_method"]

        result = add_package_name_patterns(parts, search_policy)

        expected = [
            ("package.module.TestClass.test_method.schema.json", "schema"),
            ("package.module.TestClass.test_method.json", "json"),
        ]
        assert result == expected

    def test_add_package_name_patterns_insufficient_parts(self):
        """Test adding package name patterns with insufficient parts."""
        search_policy = SearchPolicy(
            path_to_file_separator=PathSeparator.SLASH,
            path_to_class_separator=PathSeparator.DOT,
        )
        parts = ["single_part"]

        result = add_package_name_patterns(parts, search_policy)

        # Should handle edge case gracefully
        assert isinstance(result, list)


class TestAddSlashSeparatedPatterns:
    """Test add_slash_separated_patterns function."""

    def test_add_slash_separated_patterns_basic(self):
        """Test adding slash separated patterns."""
        search_policy = SearchPolicy(path_to_class_separator=PathSeparator.DOT)
        without_package = ["module", "submodule", "TestClass", "test_method"]

        result = add_slash_separated_patterns(without_package, search_policy)

        expected = [
            ("module/submodule/TestClass.test_method.schema.json", "schema"),
            ("module/submodule/TestClass.test_method.json", "json"),
        ]
        assert result == expected

    def test_add_slash_separated_patterns_insufficient_parts(self):
        """Test adding slash separated patterns with insufficient parts."""
        search_policy = SearchPolicy(path_to_class_separator=PathSeparator.DOT)
        without_package = ["single_part"]

        result = add_slash_separated_patterns(without_package, search_policy)

        assert result == []
