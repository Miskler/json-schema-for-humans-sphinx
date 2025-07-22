"""
Tests for package compatibility and error handling.
"""

import pytest

import jsoncrack_for_sphinx
from jsoncrack_for_sphinx.config import JsonCrackConfig, Theme


class TestPackageCompatibility:
    """Test package compatibility and error handling."""

    def test_package_backward_compatibility(self):
        """Test that package maintains backward compatibility."""
        # Test that old import patterns still work
        from jsoncrack_for_sphinx import setup as main_setup
        from jsoncrack_for_sphinx.core.extension import setup as ext_setup

        # Both should be the same function
        assert main_setup is ext_setup

        # Test that configuration classes are accessible from .config
        from jsoncrack_for_sphinx.config import JsonCrackConfig

        config = JsonCrackConfig()
        assert config is not None

    def test_package_error_handling(self):
        """Test that package handles errors gracefully."""
        # Test that invalid configurations don't crash
        try:
            config = JsonCrackConfig(render=None, container=None)
            # Should use defaults
            assert config.render is not None
            assert config.container is not None
            # Theme should be AUTO by default
            assert config.theme == Theme.AUTO
        except Exception as e:
            pytest.fail(f"Package should handle None values gracefully: {e}")

    def test_package_static_files(self):
        """Test that package includes static files."""
        from pathlib import Path

        # Find package directory
        package_dir = Path(jsoncrack_for_sphinx.__file__).parent
        static_dir = package_dir / "static"

        # Test that static directory exists
        assert static_dir.exists(), "Static directory should exist"
        assert static_dir.is_dir(), "Static should be a directory"

        # Test that CSS and JS files exist
        css_file = static_dir / "jsoncrack-schema.css"
        js_file = static_dir / "jsoncrack-sphinx.js"

        assert css_file.exists(), "CSS file should exist"
        assert js_file.exists(), "JavaScript file should exist"

        # Test that files are not empty
        assert css_file.stat().st_size > 0, "CSS file should not be empty"
        assert js_file.stat().st_size > 0, "JavaScript file should not be empty"
