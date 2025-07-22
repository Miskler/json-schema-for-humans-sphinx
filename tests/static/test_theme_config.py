"""
Tests for static file theme support and configuration.
"""

from pathlib import Path


class TestStaticThemeConfig:
    """Test static file theme and configuration features."""

    def test_css_theme_support(self):
        """Test CSS theme support."""
        css_path = (
            Path(__file__).parent.parent.parent
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
