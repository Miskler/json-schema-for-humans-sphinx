"""Tests for utility functions."""

from jsoncrack_for_sphinx.patterns.pattern_strategies import remove_duplicates


class TestRemoveDuplicates:
    """Test remove_duplicates function."""

    def test_remove_duplicates_basic(self):
        """Test removing duplicate patterns."""
        patterns = [
            ("test.schema.json", "schema"),
            ("test.json", "json"),
            ("test.schema.json", "schema"),  # duplicate
            ("other.json", "json"),
        ]

        result = remove_duplicates(patterns)

        expected = [
            ("test.schema.json", "schema"),
            ("test.json", "json"),
            ("other.json", "json"),
        ]
        assert result == expected

    def test_remove_duplicates_preserve_order(self):
        """Test that remove_duplicates preserves order."""
        patterns = [
            ("first.json", "json"),
            ("second.json", "json"),
            ("first.json", "json"),  # duplicate
            ("third.json", "json"),
        ]

        result = remove_duplicates(patterns)

        expected = [
            ("first.json", "json"),
            ("second.json", "json"),
            ("third.json", "json"),
        ]
        assert result == expected

    def test_remove_duplicates_empty(self):
        """Test removing duplicates from empty list."""
        patterns = []
        result = remove_duplicates(patterns)
        assert result == []

    def test_remove_duplicates_no_duplicates(self):
        """Test removing duplicates when there are none."""
        patterns = [
            ("test1.json", "json"),
            ("test2.schema.json", "schema"),
            ("test3.json", "json"),
        ]

        result = remove_duplicates(patterns)

        assert result == patterns
