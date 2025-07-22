"""
Tests for static file syntax validation.
"""

import re
from pathlib import Path


class TestCssSyntax:
    """Test CSS syntax validity."""

    def test_css_syntax_validity(self):
        """Test CSS syntax validity (basic checks)."""
        css_path = (
            Path(__file__).parent.parent.parent
            / "src"
            / "jsoncrack_for_sphinx"
            / "static"
            / "jsoncrack-schema.css"
        )

        with open(css_path, "r", encoding="utf-8") as f:
            css_content = f.read()

        # Check for balanced braces
        open_braces = css_content.count("{")
        close_braces = css_content.count("}")
        assert open_braces == close_braces, "CSS should have balanced braces"

        # Check for proper comment syntax
        if "/*" in css_content:
            assert "*/" in css_content, "CSS comments should be properly closed"

        # Check for basic CSS structure
        assert ":" in css_content, "CSS should contain property declarations"
        assert ";" in css_content, "CSS should contain statement terminators"

        # Check for no obvious syntax errors
        assert "}}" not in css_content, "CSS should not have double closing braces"
        assert "{{" not in css_content, "CSS should not have double opening braces"

    def test_css_responsive_design(self):
        """Test CSS responsive design features."""
        css_path = (
            Path(__file__).parent.parent.parent
            / "src"
            / "jsoncrack_for_sphinx"
            / "static"
            / "jsoncrack-schema.css"
        )

        with open(css_path, "r", encoding="utf-8") as f:
            css_content = f.read()

        # Check for media queries
        assert "@media" in css_content, "CSS should contain media queries"

        # Check for responsive units
        responsive_units = ["%", "rem", "em", "vw", "vh"]
        has_responsive_units = any(unit in css_content for unit in responsive_units)
        assert has_responsive_units, "CSS should use responsive units"

        # Check for flexible layouts
        assert (
            "flex" in css_content
            or "grid" in css_content
            or "width: 100%" in css_content
        ), "CSS should support flexible layouts"


class TestJavaScriptSyntax:
    """Test JavaScript syntax validity."""

    def test_js_syntax_validity(self):
        """Test JavaScript syntax validity (basic checks)."""
        js_path = (
            Path(__file__).parent.parent.parent
            / "src"
            / "jsoncrack_for_sphinx"
            / "static"
            / "jsoncrack-sphinx.js"
        )

        with open(js_path, "r", encoding="utf-8") as f:
            js_content = f.read()

        # Check for balanced parentheses in main areas
        # Note: This is a simplified check
        function_matches = re.findall(r"function\s*\([^)]*\)\s*{", js_content)
        assert (
            len(function_matches) > 0
        ), "JavaScript should contain function declarations"

        # Check for proper IIFE structure
        assert "(function()" in js_content, "JavaScript should use IIFE pattern"
        assert "})();" in js_content, "JavaScript IIFE should be properly closed"

        # Check for no obvious syntax errors
        assert (
            "var " in js_content or "const " in js_content or "let " in js_content
        ), "JavaScript should declare variables"
        assert "document." in js_content, "JavaScript should interact with DOM"

        # Check for proper string handling
        single_quotes = js_content.count("'")
        double_quotes = js_content.count('"')
        assert (
            single_quotes % 2 == 0 or double_quotes % 2 == 0
        ), "JavaScript should have balanced quotes"
