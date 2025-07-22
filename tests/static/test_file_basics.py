"""
Tests for static file existence and basic content validation.
"""

from pathlib import Path


class TestStaticFileExistence:
    """Test static file existence."""

    def test_css_file_exists(self):
        """Test that CSS file exists."""
        css_path = (
            Path(__file__).parent.parent.parent
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
            Path(__file__).parent.parent.parent
            / "src"
            / "jsoncrack_for_sphinx"
            / "static"
            / "jsoncrack-sphinx.js"
        )
        assert js_path.exists(), "JavaScript file should exist"
        assert js_path.is_file(), "JavaScript path should be a file"


class TestStaticFileContent:
    """Test static file content."""

    def test_css_file_content(self):
        """Test CSS file content and structure."""
        css_path = (
            Path(__file__).parent.parent.parent
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
            Path(__file__).parent.parent.parent
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
