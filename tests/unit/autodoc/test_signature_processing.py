"""
Tests for autodoc signature processing functionality.
"""

from unittest.mock import Mock

from jsoncrack_for_sphinx.core.autodoc import (
    autodoc_process_signature,
)


class TestAutodocProcessSignature:
    """Test autodoc signature processing."""

    def test_autodoc_process_signature_function(self, schema_dir):
        """Test processing signature for a function."""
        mock_app = Mock()
        mock_app.config = Mock()
        mock_app.config.json_schema_dir = str(schema_dir)
        mock_app.env = Mock()
        mock_app.env._jsoncrack_schema_paths = {}

        result = autodoc_process_signature(
            mock_app,
            "function",
            "example_module.process_data",
            Mock(),
            {},
            "signature",
            "return_annotation",
        )

        # Should return None (no modification to signature)
        assert result is None

        # Should store schema path in env
        assert hasattr(mock_app.env, "_jsoncrack_schema_paths")
        schema_paths = getattr(mock_app.env, "_jsoncrack_schema_paths")
        assert "example_module.process_data" in schema_paths

    def test_autodoc_process_signature_method(self, schema_dir):
        """Test processing signature for a method."""
        mock_app = Mock()
        mock_app.config = Mock()
        mock_app.config.json_schema_dir = str(schema_dir)
        mock_app.env = Mock()
        mock_app.env._jsoncrack_schema_paths = {}

        result = autodoc_process_signature(
            mock_app,
            "method",
            "example_module.User.create",
            Mock(),
            {},
            "signature",
            "return_annotation",
        )

        assert result is None

        schema_paths = getattr(mock_app.env, "_jsoncrack_schema_paths")
        assert "example_module.User.create" in schema_paths

    def test_autodoc_process_signature_no_schema_dir(self):
        """Test processing signature when no schema directory is configured."""
        mock_app = Mock()
        mock_app.config = Mock()
        mock_app.config.json_schema_dir = None
        mock_app.env = Mock()

        result = autodoc_process_signature(
            mock_app,
            "function",
            "example_module.process_data",
            Mock(),
            {},
            "signature",
            "return_annotation",
        )

        assert result is None

    def test_autodoc_process_signature_not_supported_type(self, schema_dir):
        """Test processing signature for unsupported object type."""
        mock_app = Mock()
        mock_app.config = Mock()
        mock_app.config.json_schema_dir = str(schema_dir)
        mock_app.env = Mock()

        result = autodoc_process_signature(
            mock_app,
            "attribute",
            "example_module.some_attr",
            Mock(),
            {},
            "signature",
            "return_annotation",
        )

        assert result is None

    def test_autodoc_process_signature_schema_not_found(self, schema_dir):
        """Test processing signature when schema is not found."""
        mock_app = Mock()
        mock_app.config = Mock()
        mock_app.config.json_schema_dir = str(schema_dir)
        mock_app.env = Mock()

        result = autodoc_process_signature(
            mock_app,
            "function",
            "example_module.non_existent_function",
            Mock(),
            {},
            "signature",
            "return_annotation",
        )

        assert result is None
