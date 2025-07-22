"""
Feature compatibility tests across different environments.
"""


class TestFeatureCompatibility:
    """Test feature compatibility across different environments."""

    def test_file_encoding_compatibility(self, temp_dir):
        """Test file encoding compatibility."""
        from jsoncrack_for_sphinx.schema.schema_utils import (
            get_schema_info,
            validate_schema_file,
        )

        # Test UTF-8 encoding
        utf8_schema = {
            "type": "object",
            "title": "UTF-8 Test with émojis 🚀",
            "properties": {"café": {"type": "string"}, "naïve": {"type": "string"}},
        }

        utf8_file = temp_dir / "utf8.schema.json"
        with open(utf8_file, "w", encoding="utf-8") as f:
            import json

            json.dump(utf8_schema, f, ensure_ascii=False)

        assert validate_schema_file(utf8_file) is True
        info = get_schema_info(utf8_file)
        assert "UTF-8 Test with émojis 🚀" in info["title"]
        assert "café" in info["properties"]

    def test_html_escaping_compatibility(self, temp_dir):
        """Test HTML escaping compatibility."""
        from jsoncrack_for_sphinx.generators.html_generator import generate_schema_html

        # Create schema with HTML-like content
        html_schema = {
            "type": "object",
            "title": "HTML Test <script>alert('xss')</script>",
            "properties": {
                "content": {
                    "type": "string",
                    "description": "Contains <b>HTML</b> & special chars",
                }
            },
        }

        schema_file = temp_dir / "html_test.schema.json"
        with open(schema_file, "w") as f:
            import json

            json.dump(html_schema, f)

        html = generate_schema_html(schema_file, "schema")

        # Should be properly escaped
        assert "jsoncrack-container" in html
        assert "&lt;script&gt;" in html or "script" not in html  # Should be escaped
        assert "data-schema=" in html  # JSON data should be present
