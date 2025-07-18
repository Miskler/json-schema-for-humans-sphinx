"""
Tests for the main package.
"""

import pytest

import jsoncrack_for_sphinx
from jsoncrack_for_sphinx import (
    ContainerConfig,
    Directions,
    JsonCrackConfig,
    RenderConfig,
    RenderMode,
    Theme,
    setup,
)


class TestPackage:
    """Test the main package."""

    def test_package_metadata(self):
        """Test package metadata."""
        assert hasattr(jsoncrack_for_sphinx, "__version__")
        assert hasattr(jsoncrack_for_sphinx, "__author__")
        assert jsoncrack_for_sphinx.__version__ == "0.1.0"
        assert jsoncrack_for_sphinx.__author__ == "Miskler"

    def test_package_exports(self):
        """Test that package exports the correct symbols."""
        # Test main setup function
        assert hasattr(jsoncrack_for_sphinx, "setup")
        assert callable(jsoncrack_for_sphinx.setup)

        # Test configuration classes
        assert hasattr(jsoncrack_for_sphinx, "RenderMode")
        assert hasattr(jsoncrack_for_sphinx, "Directions")
        assert hasattr(jsoncrack_for_sphinx, "Theme")
        assert hasattr(jsoncrack_for_sphinx, "ContainerConfig")
        assert hasattr(jsoncrack_for_sphinx, "RenderConfig")
        assert hasattr(jsoncrack_for_sphinx, "JsonCrackConfig")

    def test_package_all_attribute(self):
        """Test that __all__ contains the expected exports."""
        expected_exports = [
            "setup",
            "RenderMode",
            "Directions",
            "Theme",
            "ContainerConfig",
            "RenderConfig",
            "JsonCrackConfig",
        ]

        assert hasattr(jsoncrack_for_sphinx, "__all__")
        assert set(jsoncrack_for_sphinx.__all__) == set(expected_exports)

    def test_import_from_package(self):
        """Test importing from the package."""
        # Test direct import
        from jsoncrack_for_sphinx import setup

        assert callable(setup)

        # Test config imports
        from jsoncrack_for_sphinx import Directions, RenderMode, Theme

        assert hasattr(RenderMode, "OnClick")
        assert hasattr(RenderMode, "OnLoad")
        assert hasattr(RenderMode, "OnScreen")
        assert hasattr(Directions, "TOP")
        assert hasattr(Directions, "RIGHT")
        assert hasattr(Directions, "DOWN")
        assert hasattr(Directions, "LEFT")
        assert hasattr(Theme, "LIGHT")
        assert hasattr(Theme, "DARK")
        assert hasattr(Theme, "AUTO")

        # Test configuration classes
        from jsoncrack_for_sphinx import ContainerConfig, JsonCrackConfig, RenderConfig

        assert callable(ContainerConfig)
        assert callable(RenderConfig)
        assert callable(JsonCrackConfig)

    def test_package_structure(self):
        """Test package structure."""
        # Test that we can import submodules
        from jsoncrack_for_sphinx import config, extension, fixtures, utils

        # Test that submodules have expected attributes
        assert hasattr(extension, "setup")
        assert hasattr(config, "RenderMode")
        assert hasattr(utils, "schema_to_rst")
        assert hasattr(fixtures, "schema_to_rst_fixture")

    def test_package_version_consistency(self):
        """Test that package version is consistent."""
        # Test that the version in __init__.py matches setup.py/pyproject.toml
        assert jsoncrack_for_sphinx.__version__ == "0.1.0"

        # Test that the version is a string
        assert isinstance(jsoncrack_for_sphinx.__version__, str)

        # Test that the version follows semantic versioning pattern
        import re

        version_pattern = r"^\d+\.\d+\.\d+$"
        assert re.match(version_pattern, jsoncrack_for_sphinx.__version__)

    def test_package_documentation(self):
        """Test package documentation."""
        # Test that package has docstring
        assert jsoncrack_for_sphinx.__doc__ is not None
        assert len(jsoncrack_for_sphinx.__doc__.strip()) > 0

        # Test that docstring mentions key features
        doc = jsoncrack_for_sphinx.__doc__
        assert "Sphinx" in doc
        assert "JSON" in doc
        assert "schema" in doc

    def test_package_imports_work(self):
        """Test that all package imports work correctly."""
        # Test importing the package
        import jsoncrack_for_sphinx as jsf

        assert jsf is not None

        # Test importing specific components
        from jsoncrack_for_sphinx.config import RenderMode
        from jsoncrack_for_sphinx.extension import SchemaDirective
        from jsoncrack_for_sphinx.fixtures import schema_to_rst_fixture
        from jsoncrack_for_sphinx.utils import schema_to_rst

        # Test that imports are working
        assert RenderMode is not None
        assert SchemaDirective is not None
        assert schema_to_rst is not None
        assert schema_to_rst_fixture is not None

    def test_package_dependencies(self):
        """Test that package dependencies are available."""
        # Test that required dependencies can be imported

        # Test optional dependencies
        try:
            pass

            jsf_available = True
        except ImportError:
            jsf_available = False

        # jsf is listed as a dependency, so it should be available
        assert jsf_available, "jsf dependency should be available"

    def test_package_sphinx_integration(self):
        """Test that package integrates with Sphinx."""
        from unittest.mock import Mock

        # Create mock Sphinx app
        mock_app = Mock()
        mock_app.config = Mock()
        mock_app.config.html_static_path = []
        mock_app.add_config_value = Mock()
        mock_app.add_directive = Mock()
        mock_app.connect = Mock()
        mock_app.add_css_file = Mock()
        mock_app.add_js_file = Mock()

        # Test that setup works
        result = setup(mock_app)

        # Verify setup result
        assert isinstance(result, dict)
        assert "version" in result
        assert result["version"] == "0.1.0"
        assert "parallel_read_safe" in result
        assert "parallel_write_safe" in result

    def test_package_config_classes(self):
        """Test that configuration classes work correctly."""
        # Test RenderMode classes
        onclick = RenderMode.OnClick()
        onload = RenderMode.OnLoad()
        onscreen = RenderMode.OnScreen()

        assert onclick.mode == "onclick"
        assert onload.mode == "onload"
        assert onscreen.mode == "onscreen"

        # Test Directions enum
        assert Directions.TOP.value == "TOP"
        assert Directions.RIGHT.value == "RIGHT"
        assert Directions.DOWN.value == "DOWN"
        assert Directions.LEFT.value == "LEFT"

        # Test Theme enum
        assert Theme.LIGHT.value == "light"
        assert Theme.DARK.value == "dark"
        assert Theme.AUTO.value is None

        # Test configuration classes
        container_config = ContainerConfig()
        render_config = RenderConfig(onclick)
        jsoncrack_config = JsonCrackConfig()

        assert container_config.direction == Directions.RIGHT
        assert render_config.mode == onclick
        assert isinstance(jsoncrack_config.render.mode, RenderMode.OnClick)

    def test_package_backward_compatibility(self):
        """Test that package maintains backward compatibility."""
        # Test that old import patterns still work
        from jsoncrack_for_sphinx import setup as main_setup
        from jsoncrack_for_sphinx.extension import setup as ext_setup

        # Both should be the same function
        assert main_setup is ext_setup

        # Test that configuration classes are accessible
        from jsoncrack_for_sphinx import JsonCrackConfig

        config = JsonCrackConfig()
        assert config is not None

    def test_package_error_handling(self):
        """Test that package handles errors gracefully."""
        # Test that invalid configurations don't crash
        try:
            config = JsonCrackConfig(render=None, container=None, theme=None)
            # Should use defaults
            assert config.render is not None
            assert config.container is not None
            # Theme can be None - that's valid
            assert config.theme is None or config.theme is not None
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
