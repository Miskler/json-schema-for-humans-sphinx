"""
Tests for static file functionality (responsive design, accessibility, performance).
"""

from pathlib import Path


class TestStaticFunctionality:
    """Test static file functionality features."""

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

    def test_js_configuration_handling(self):
        """Test JavaScript configuration handling."""
        js_path = (
            Path(__file__).parent.parent.parent
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
            Path(__file__).parent.parent.parent
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
            Path(__file__).parent.parent.parent
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
            Path(__file__).parent.parent.parent
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

    def test_js_performance_features(self):
        """Test JavaScript performance features."""
        js_path = (
            Path(__file__).parent.parent.parent
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
