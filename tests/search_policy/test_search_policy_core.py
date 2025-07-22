"""
Tests for PathSeparator enum and SearchPolicy class.
"""

from jsoncrack_for_sphinx.config import PathSeparator, SearchPolicy


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
            custom_patterns=custom_patterns,
        )

        assert policy.include_package_name is True
        assert policy.path_to_file_separator == PathSeparator.SLASH
        assert policy.path_to_class_separator == PathSeparator.NONE
        assert policy.custom_patterns == custom_patterns

    def test_search_policy_representation(self):
        """Test SearchPolicy string representation."""
        policy = SearchPolicy(
            include_package_name=True, path_to_file_separator=PathSeparator.SLASH
        )

        repr_str = repr(policy)
        assert "SearchPolicy" in repr_str
        assert "include_package_name=True" in repr_str
        assert "path_to_file_separator=PathSeparator.SLASH" in repr_str
