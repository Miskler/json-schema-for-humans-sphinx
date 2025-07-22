"""Tests for custom pattern processing."""

from jsoncrack_for_sphinx.patterns.custom_patterns import process_custom_patterns
from jsoncrack_for_sphinx.search.search_policy import SearchPolicy


class TestProcessCustomPatterns:
    """Test custom pattern processing."""

    def test_process_custom_patterns_with_class_method(self):
        """Test custom pattern processing with class and method placeholders."""
        search_policy = SearchPolicy(
            custom_patterns=[
                "{class_name}_{method_name}",
                "custom_{object_name}",
                "patterns/{class_name}/{method_name}",
            ]
        )
        parts = ["package", "module", "TestClass", "test_method"]
        obj_name = "TestClass.test_method"

        result = process_custom_patterns(parts, obj_name, search_policy)

        # Should expand placeholders and add extensions
        expected = [
            ("TestClass_test_method.schema.json", "schema"),
            ("TestClass_test_method.json", "json"),
            ("custom_TestClass.test_method.schema.json", "schema"),
            ("custom_TestClass.test_method.json", "json"),
            ("patterns/TestClass/test_method.schema.json", "schema"),
            ("patterns/TestClass/test_method.json", "json"),
        ]
        assert result == expected

    def test_process_custom_patterns_with_extension(self):
        """Test custom patterns that already include file extensions."""
        search_policy = SearchPolicy(
            custom_patterns=[
                "{class_name}_{method_name}.schema.json",
                "custom_{object_name}.json",
            ]
        )
        parts = ["package", "module", "TestClass", "test_method"]
        obj_name = "TestClass.test_method"

        result = process_custom_patterns(parts, obj_name, search_policy)

        # Should not add additional extensions
        expected = [
            ("TestClass_test_method.schema.json", "schema"),
            ("custom_TestClass.test_method.json", "json"),
        ]
        assert result == expected

    def test_process_custom_patterns_insufficient_parts(self):
        """Test custom pattern processing with insufficient parts."""
        search_policy = SearchPolicy(
            custom_patterns=["{class_name}_{method_name}", "single_{object_name}"]
        )
        parts = ["single_part"]
        obj_name = "single_part"

        result = process_custom_patterns(parts, obj_name, search_policy)

        # Should only replace object_name placeholder
        expected = [
            ("{class_name}_{method_name}.schema.json", "schema"),
            ("{class_name}_{method_name}.json", "json"),
            ("single_single_part.schema.json", "schema"),
            ("single_single_part.json", "json"),
        ]
        assert result == expected

    def test_process_custom_patterns_empty(self):
        """Test custom pattern processing with no custom patterns."""
        search_policy = SearchPolicy(custom_patterns=[])
        parts = ["package", "module", "TestClass", "test_method"]
        obj_name = "TestClass.test_method"

        result = process_custom_patterns(parts, obj_name, search_policy)

        assert result == []

    def test_process_custom_patterns_object_name_only(self):
        """Test custom pattern processing with object name placeholder only."""
        search_policy = SearchPolicy(
            custom_patterns=["schema_{object_name}", "data/{object_name}"]
        )
        parts = ["package", "module", "TestClass", "test_method"]
        obj_name = "TestClass.test_method"

        result = process_custom_patterns(parts, obj_name, search_policy)

        expected = [
            ("schema_TestClass.test_method.schema.json", "schema"),
            ("schema_TestClass.test_method.json", "json"),
            ("data/TestClass.test_method.schema.json", "schema"),
            ("data/TestClass.test_method.json", "json"),
        ]
        assert result == expected
