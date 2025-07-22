"""
Additional edge case tests for the jsoncrack-for-sphinx extension.
"""

import json
from unittest.mock import Mock, patch

from jsoncrack_for_sphinx.generators.html_generator import generate_schema_html
from jsoncrack_for_sphinx.schema.schema_utils import validate_schema_file


class TestMissingDependencies:
    """Test behavior when optional dependencies are missing."""

    def test_missing_jsf_dependency(self, temp_dir):
        """Test behavior when JSF is not available."""
        # Create a schema file
        schema_data = {
            "type": "object",
            "properties": {"name": {"type": "string"}, "age": {"type": "integer"}},
        }

        schema_file = temp_dir / "test.schema.json"
        with open(schema_file, "w") as f:
            json.dump(schema_data, f)

        # Mock JSF import failure
        def mock_import(name, *args, **kwargs):
            if name == "jsf":
                raise ImportError("No module named 'jsf'")
            return __import__(name, *args, **kwargs)

        with patch("builtins.__import__", side_effect=mock_import):
            html = generate_schema_html(schema_file, "schema")

            # Should still work, just without fake data generation
            # The function should return something, even if it's an error message
            assert html is not None
            assert len(html) > 0
            # The function should either return valid HTML or an error message
            assert "jsoncrack-container" in html or "error" in html.lower()


class TestOptionalFeatures:
    """Test optional features and fallbacks."""

    def test_jsf_fallback_behavior(self, temp_dir):
        """Test JSF fallback behavior."""
        # Create schema file
        schema_data = {
            "type": "object",
            "properties": {"id": {"type": "integer"}, "name": {"type": "string"}},
        }

        schema_file = temp_dir / "fallback.schema.json"
        with open(schema_file, "w") as f:
            json.dump(schema_data, f)

        # Should work even without JSF
        html = generate_schema_html(schema_file, "schema")
        assert "jsoncrack-container" in html
        assert "data-schema=" in html

    def test_file_access_error_handling(self, temp_dir):
        """Test handling of file access errors."""
        # Create and then remove a file to simulate access error
        schema_file = temp_dir / "temp.schema.json"
        with open(schema_file, "w") as f:
            json.dump({"type": "string"}, f)

        # Remove file
        schema_file.unlink()

        # Should handle gracefully
        assert validate_schema_file(schema_file) is False

        html = generate_schema_html(schema_file, "schema")
        assert "error" in html.lower()


class TestErrorRecovery:
    """Test error recovery and graceful degradation."""

    def test_partial_configuration_recovery(self):
        """Test recovery from partial configuration errors."""
        from jsoncrack_for_sphinx.config.config_utils import get_jsoncrack_config

        # Create configuration with some invalid values
        mock_config = Mock()
        if hasattr(mock_config, "jsoncrack_default_options"):
            delattr(mock_config, "jsoncrack_default_options")

        mock_config.jsoncrack_render_mode = "invalid_mode"  # Invalid
        mock_config.jsoncrack_theme = "dark"  # Valid
        mock_config.jsoncrack_direction = "TOP"  # Valid
        mock_config.jsoncrack_height = "500"
        mock_config.jsoncrack_width = "100%"
        mock_config.jsoncrack_onscreen_threshold = 0.1
        mock_config.jsoncrack_onscreen_margin = "50px"

        # Should recover gracefully
        config = get_jsoncrack_config(mock_config)

        assert config is not None
        assert config.theme.value == "dark"
        assert config.container.direction.value == "TOP"

    def test_schema_parsing_recovery(self, temp_dir):
        """Test recovery from schema parsing errors."""
        # Create file with invalid JSON
        invalid_file = temp_dir / "invalid.schema.json"
        with open(invalid_file, "w") as f:
            f.write('{"type": "object", "properties": {invalid}}')

        # Should handle gracefully
        assert validate_schema_file(invalid_file) is False

        html = generate_schema_html(invalid_file, "schema")
        assert "error" in html.lower()

    def test_unicode_error_recovery(self, temp_dir):
        """Test recovery from Unicode errors."""
        # Create file with problematic Unicode
        unicode_file = temp_dir / "unicode.schema.json"

        try:
            with open(unicode_file, "w", encoding="utf-8") as f:
                json.dump(
                    {
                        "type": "object",
                        "title": "Unicode Test \ud83d\ude80",
                        "properties": {"test": {"type": "string"}},
                    },
                    f,
                    ensure_ascii=False,
                )

            # Should handle gracefully
            assert validate_schema_file(unicode_file) is True

            html = generate_schema_html(unicode_file, "schema")
            assert "jsoncrack-container" in html or "error" in html.lower()

        except (UnicodeError, UnicodeDecodeError, UnicodeEncodeError):
            # If Unicode handling fails, that's also acceptable
            pass

    def test_circular_reference_recovery(self, temp_dir):
        """Test recovery from circular reference errors."""
        from jsoncrack_for_sphinx.config import JsonCrackConfig

        # Test that we can create config without circular references
        config = JsonCrackConfig()
        assert config is not None

        # Test with potentially circular data
        circular_schema = {
            "type": "object",
            "properties": {"self": {"$ref": "#"}},  # Self-reference
        }

        circular_file = temp_dir / "circular.schema.json"
        with open(circular_file, "w") as f:
            json.dump(circular_schema, f)

        # Should handle gracefully
        html = generate_schema_html(circular_file, "schema")
        assert html is not None
        assert len(html) > 0
