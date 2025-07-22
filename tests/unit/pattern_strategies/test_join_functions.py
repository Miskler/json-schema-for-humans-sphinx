"""Tests for join functions."""

from jsoncrack_for_sphinx.patterns.pattern_strategies import join_with_separator
from jsoncrack_for_sphinx.utils.types import PathSeparator


class TestJoinWithSeparator:
    """Test join_with_separator function."""

    def test_join_with_dot_separator(self):
        """Test joining with dot separator."""
        parts = ["package", "module", "class"]
        result = join_with_separator(parts, PathSeparator.DOT)
        assert result == "package.module.class"

    def test_join_with_slash_separator(self):
        """Test joining with slash separator."""
        parts = ["package", "module", "class"]
        result = join_with_separator(parts, PathSeparator.SLASH)
        assert result == "package/module/class"

    def test_join_with_none_separator(self):
        """Test joining with no separator."""
        parts = ["package", "module", "class"]
        result = join_with_separator(parts, PathSeparator.NONE)
        assert result == "packagemoduleclass"

    def test_join_with_unknown_separator(self):
        """Test joining with unknown separator falls back to dot."""
        parts = ["package", "module", "class"]
        # Test fallback behavior by using a separator value that's not handled

        class MockSeparator:
            pass

        result = join_with_separator(parts, MockSeparator())
        assert result == "package.module.class"
