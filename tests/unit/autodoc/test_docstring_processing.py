"""
Tests for autodoc docstring processing functionality.
"""

from unittest.mock import Mock

from jsoncrack_for_sphinx.core.autodoc import (
    autodoc_process_docstring,
)


class TestAutodocProcessDocstring:
    """Test autodoc docstring processing."""

    def test_autodoc_process_docstring_with_schema(self, schema_dir):
        """Test processing docstring with schema data."""
        mock_app = Mock()
        mock_app.config = Mock()
        mock_app.config.jsoncrack_default_options = {}
        mock_app.env = Mock()
        mock_app.env._jsoncrack_schema_paths = {
            "example_module.User.create": (
                str(schema_dir / "User.create.schema.json"),
                "schema",
            )
        }

        lines = ["Function description", "", "Args:", "    data: Input data"]

        autodoc_process_docstring(
            mock_app, "method", "example_module.User.create", Mock(), {}, lines
        )

        # Should add schema HTML to docstring
        assert len(lines) > 4
        assert any(".. raw:: html" in line for line in lines)
        assert any("jsoncrack-container" in line for line in lines)

    def test_autodoc_process_docstring_no_schema_paths(self):
        """Test processing docstring when no schema paths are stored."""
        mock_app = Mock()
        mock_app.config = Mock()
        mock_app.env = Mock()
        # Explicitly remove the _jsoncrack_schema_paths attribute
        if hasattr(mock_app.env, "_jsoncrack_schema_paths"):
            delattr(mock_app.env, "_jsoncrack_schema_paths")

        lines = ["Function description"]
        original_lines = lines.copy()

        autodoc_process_docstring(
            mock_app, "function", "example_module.some_function", Mock(), {}, lines
        )

        # Should not modify lines
        assert lines == original_lines

    def test_autodoc_process_docstring_no_matching_schema(self, schema_dir):
        """Test processing docstring when no matching schema is found."""
        mock_app = Mock()
        mock_app.config = Mock()
        mock_app.env = Mock()
        mock_app.env._jsoncrack_schema_paths = {
            "example_module.other_function": (
                str(schema_dir / "other.schema.json"),
                "schema",
            )
        }

        lines = ["Function description"]
        original_lines = lines.copy()

        autodoc_process_docstring(
            mock_app, "function", "example_module.some_function", Mock(), {}, lines
        )

        # Should not modify lines
        assert lines == original_lines

    def test_autodoc_process_docstring_legacy_format(self, schema_dir):
        """Test processing docstring with legacy schema path format."""
        mock_app = Mock()
        mock_app.config = Mock()
        mock_app.env = Mock()
        mock_app.env._jsoncrack_schema_paths = {
            "example_module.User.create": str(schema_dir / "User.create.schema.json")
        }

        lines = ["Function description"]

        autodoc_process_docstring(
            mock_app, "method", "example_module.User.create", Mock(), {}, lines
        )

        # Should add schema HTML to docstring
        assert len(lines) > 1
        assert any(".. raw:: html" in line for line in lines)

    def test_autodoc_process_docstring_unsupported_type(self, schema_dir):
        """Test processing docstring for unsupported object type."""
        mock_app = Mock()
        mock_app.config = Mock()
        mock_app.env = Mock()
        mock_app.env._jsoncrack_schema_paths = {
            "example_module.some_attr": (str(schema_dir / "some.schema.json"), "schema")
        }

        lines = ["Attribute description"]
        original_lines = lines.copy()

        autodoc_process_docstring(
            mock_app, "attribute", "example_module.some_attr", Mock(), {}, lines
        )

        # Should not modify lines
        assert lines == original_lines
