"""
Tests for static files (CSS and JavaScript).
"""

import re
from pathlib import Path


class TestStaticFiles:
    """Test static CSS and JavaScript files."""

    def test_css_file_exists(self):
        """Test that CSS file exists."""
        css_path = (
            Path(__file__).parent.parent
            / "src"
            / "jsoncrack_for_sphinx"
            / "static"
            / "jsoncrack-schema.css"
        )
        assert css_path.exists(), "CSS file should exist"
        assert css_path.is_file(), "CSS path should be a file"

    def test_js_file_exists(self):
        """Test that JavaScript file exists."""
        js_path = (
            Path(__file__).parent.parent
            / "src"
            / "jsoncrack_for_sphinx"
            / "static"
            / "jsoncrack-sphinx.js"
        )
        assert js_path.exists(), "JavaScript file should exist"
        assert js_path.is_file(), "JavaScript path should be a file"

    def test_css_file_content(self):
        """Test CSS file content and structure."""
        css_path = (
            Path(__file__).parent.parent
            / "src"
            / "jsoncrack_for_sphinx"
            / "static"
            / "jsoncrack-schema.css"
        )

        with open(css_path, "r", encoding="utf-8") as f:
            css_content = f.read()

        # Check for essential CSS classes
        assert ".jsoncrack-container" in css_content
        assert ".jsoncrack-button" in css_content
        assert ".json-schema-container" in css_content

        # Check for render mode specific styles
        assert 'data-render-mode="onclick"' in css_content
        assert 'data-render-mode="onscreen"' in css_content

        # Check for dark mode support
        assert "@media (prefers-color-scheme: dark)" in css_content

        # Check for basic styling properties
        assert "border" in css_content
        assert "background" in css_content
        assert "color" in css_content

        # Check for animation/transition properties
        assert "transition" in css_content

        # Verify CSS is not empty
        assert len(css_content.strip()) > 0

    def test_js_file_content(self):
        """Test JavaScript file content and structure."""
        js_path = (
            Path(__file__).parent.parent
            / "src"
            / "jsoncrack_for_sphinx"
            / "static"
            / "jsoncrack-sphinx.js"
        )

        with open(js_path, "r", encoding="utf-8") as f:
            js_content = f.read()

        # Check for essential functions
        assert "initJsonCrackContainers" in js_content
        assert "setupContainer" in js_content
        assert "sendDataToIframe" in js_content
        assert "getActualTheme" in js_content
        assert "getLocalizedText" in js_content

        # Check for render mode handling
        assert "renderMode" in js_content
        assert "onclick" in js_content
        assert "onload" in js_content
        assert "onscreen" in js_content

        # Check for JSONCrack integration
        assert "jsoncrack.com" in js_content
        assert "postMessage" in js_content

        # Check for event handling
        assert "addEventListener" in js_content
        assert "DOMContentLoaded" in js_content

        # Check for localization support
        assert "getLocalizedText" in js_content
        assert "ru" in js_content  # Russian localization
        assert "en" in js_content  # English localization

        # Verify JavaScript is not empty
        assert len(js_content.strip()) > 0

    def test_css_syntax_validity(self):
        """Test CSS syntax validity (basic checks)."""
        css_path = (
            Path(__file__).parent.parent
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

    def test_js_syntax_validity(self):
        """Test JavaScript syntax validity (basic checks)."""
        js_path = (
            Path(__file__).parent.parent
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

    def test_css_responsive_design(self):
        """Test CSS responsive design features."""
        css_path = (
            Path(__file__).parent.parent
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

    def test_js_configuration_handling(self):
        """Test JavaScript configuration handling."""
        js_path = (
            Path(__file__).parent.parent
            / "src"
            / "jsoncrack_for_sphinx"
            / "static"
            / "jsoncrack-sphinx.js"
        )

        with open(js_path, "r", encoding="utf-8") as f:
            js_content = f.read()

        # Check for configuration constants
        assert "DEFAULT_CONFIG" in js_content

        # Check for all configuration options
        config_options = [
            "renderMode",
            "theme",
            "direction",
            "height",
            "width",
            "onscreenThreshold",
            "onscreenMargin",
        ]

        for option in config_options:
            assert (
                option in js_content
            ), f"JavaScript should handle {option} configuration"

        # Check for data attribute handling
        assert "dataset" in js_content, "JavaScript should handle HTML data attributes"
        assert (
            "dataset." in js_content
        ), "JavaScript should access data attributes via dataset"

    def test_js_accessibility(self):
        """Test JavaScript accessibility features."""
        js_path = (
            Path(__file__).parent.parent
            / "src"
            / "jsoncrack_for_sphinx"
            / "static"
            / "jsoncrack-sphinx.js"
        )

        with open(js_path, "r", encoding="utf-8") as f:
            js_content = f.read()

        # Check for keyboard accessibility
        assert "button" in js_content, "JavaScript should create accessible buttons"

        # Check for screen reader support
        assert (
            "textContent" in js_content
        ), "JavaScript should set accessible text content"

        # Check for proper ARIA or semantic HTML
        # (This would be more comprehensive in a real accessibility audit)
        assert "click" in js_content, "JavaScript should handle click events"

    def test_css_browser_compatibility(self):
        """Test CSS browser compatibility features."""
        css_path = (
            Path(__file__).parent.parent
            / "src"
            / "jsoncrack_for_sphinx"
            / "static"
            / "jsoncrack-schema.css"
        )

        with open(css_path, "r", encoding="utf-8") as f:
            css_content = f.read()

        # Check for fallback styles
        assert (
            "background-color" in css_content
        ), "CSS should have basic background colors"
        assert "color:" in css_content, "CSS should have basic text colors"

        # Check for vendor prefixes where needed (if any)
        # This would be more comprehensive with actual CSS parsing

        # Check for progressive enhancement
        assert "transition" in css_content, "CSS should include transition effects"
        assert "box-shadow" in css_content, "CSS should include modern effects"

    def test_js_error_handling(self):
        """Test JavaScript error handling."""
        js_path = (
            Path(__file__).parent.parent
            / "src"
            / "jsoncrack_for_sphinx"
            / "static"
            / "jsoncrack-sphinx.js"
        )

        with open(js_path, "r", encoding="utf-8") as f:
            js_content = f.read()

        # Check for error handling
        assert (
            "try" in js_content or "catch" in js_content
        ), "JavaScript should include error handling"

        # Check for console logging
        assert "console." in js_content, "JavaScript should include console logging"

        # Check for graceful degradation
        assert (
            "exists" in js_content or "null" in js_content
        ), "JavaScript should check for existence"

    def test_css_theme_support(self):
        """Test CSS theme support."""
        css_path = (
            Path(__file__).parent.parent
            / "src"
            / "jsoncrack_for_sphinx"
            / "static"
            / "jsoncrack-schema.css"
        )

        with open(css_path, "r", encoding="utf-8") as f:
            css_content = f.read()

        # Check for light theme colors
        light_colors = ["#f6f8fa", "#e1e4e8", "#24292e", "#0366d6"]
        has_light_colors = any(color in css_content for color in light_colors)
        assert has_light_colors, "CSS should include light theme colors"

        # Check for dark theme colors
        dark_colors = ["#0d1117", "#21262d", "#30363d", "#79c0ff"]
        has_dark_colors = any(color in css_content for color in dark_colors)
        assert has_dark_colors, "CSS should include dark theme colors"

        # Check for theme-specific selectors
        assert (
            "prefers-color-scheme" in css_content
        ), "CSS should support system theme preference"

    def test_js_performance_features(self):
        """Test JavaScript performance features."""
        js_path = (
            Path(__file__).parent.parent
            / "src"
            / "jsoncrack_for_sphinx"
            / "static"
            / "jsoncrack-sphinx.js"
        )

        with open(js_path, "r", encoding="utf-8") as f:
            js_content = f.read()

        # Check for lazy loading
        assert (
            "IntersectionObserver" in js_content
        ), "JavaScript should support lazy loading"

        # Check for event delegation
        assert "addEventListener" in js_content, "JavaScript should use event listeners"

        # Check for DOM optimization
        assert (
            "querySelector" in js_content
        ), "JavaScript should use efficient DOM queries"

        # Check for initialization optimization
        assert (
            "DOMContentLoaded" in js_content
        ), "JavaScript should optimize initialization"

    def test_static_files_size(self):
        """Test that static files are reasonably sized."""
        css_path = (
            Path(__file__).parent.parent
            / "src"
            / "jsoncrack_for_sphinx"
            / "static"
            / "jsoncrack-schema.css"
        )
        js_path = (
            Path(__file__).parent.parent
            / "src"
            / "jsoncrack_for_sphinx"
            / "static"
            / "jsoncrack-sphinx.js"
        )

        # Check file sizes (reasonable limits)
        css_size = css_path.stat().st_size
        js_size = js_path.stat().st_size

        # CSS should be between 1KB and 100KB
        assert (
            1024 < css_size < 100 * 1024
        ), f"CSS file size should be reasonable, got {css_size} bytes"

        # JavaScript should be between 1KB and 200KB
        assert (
            1024 < js_size < 200 * 1024
        ), f"JavaScript file size should be reasonable, got {js_size} bytes"

        # Files should not be empty
        assert css_size > 0, "CSS file should not be empty"
        assert js_size > 0, "JavaScript file should not be empty"
