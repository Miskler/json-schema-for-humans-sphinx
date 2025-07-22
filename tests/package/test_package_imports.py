"""
Tests for package imports and structure.
"""

import jsoncrack_for_sphinx
from jsoncrack_for_sphinx.config import (
    Directions,
    RenderMode,
    Theme,
)


class TestPackageImports:
    """Test package imports and exports."""

    def test_package_exports(self):
        """Test that package exports the correct symbols."""
        # Test main setup function
        assert hasattr(jsoncrack_for_sphinx, "setup")
        assert callable(jsoncrack_for_sphinx.setup)

        # Test that configuration classes are NOT in main package
        # They should be imported from .config explicitly
        assert not hasattr(jsoncrack_for_sphinx, "RenderMode")
        assert not hasattr(jsoncrack_for_sphinx, "Directions")
        assert not hasattr(jsoncrack_for_sphinx, "Theme")
        assert not hasattr(jsoncrack_for_sphinx, "ContainerConfig")
        assert not hasattr(jsoncrack_for_sphinx, "RenderConfig")
        assert not hasattr(jsoncrack_for_sphinx, "JsonCrackConfig")

    def test_package_all_attribute(self):
        """Test that __all__ contains the expected exports."""
        expected_exports = [
            "setup",
        ]

        assert hasattr(jsoncrack_for_sphinx, "__all__")
        assert set(jsoncrack_for_sphinx.__all__) == set(expected_exports)

    def test_import_from_package(self):
        """Test importing specific items from the package."""
        # Test direct imports from main package
        from jsoncrack_for_sphinx import setup

        assert callable(setup)

        # Test imports from config submodule
        assert hasattr(RenderMode, "OnClick")
        assert hasattr(RenderMode, "OnScreen")
        assert hasattr(RenderMode, "OnLoad")

        # Test imports from config.directions
        assert hasattr(Directions, "LEFT")
        assert hasattr(Directions, "RIGHT")

        # Test imports from config.theme
        assert hasattr(Theme, "LIGHT")
        assert hasattr(Theme, "DARK")

        # Test configuration classes
        from jsoncrack_for_sphinx.config import (
            ContainerConfig,
            JsonCrackConfig,
            RenderConfig,
        )

        assert callable(ContainerConfig)
        assert callable(RenderConfig)
        assert callable(JsonCrackConfig)

    def test_package_structure(self):
        """Test package structure."""
        # Test that we can import submodules
        from jsoncrack_for_sphinx import config, extension, utils

        # Test that submodules have expected attributes
        assert hasattr(extension, "setup")
        assert hasattr(config, "RenderMode")
        assert hasattr(utils, "schema_to_rst")

    def test_package_imports_work(self):
        """Test that all expected imports work without errors."""
        # Test basic imports
        import jsoncrack_for_sphinx.config
        import jsoncrack_for_sphinx.extension  # noqa: F401

        # Test that we can import specific functions
        from jsoncrack_for_sphinx.core.extension import setup
        from jsoncrack_for_sphinx.generators.rst_generator import schema_to_rst

        # Test that imported items are callable/usable
        assert callable(setup)
        assert callable(schema_to_rst)

        # Test more specific imports
        from jsoncrack_for_sphinx.config import Directions, RenderMode, Theme

        assert RenderMode.OnClick().mode == "onclick"
        assert Theme.LIGHT.value == "light"
        assert Directions.LEFT.value == "LEFT"

    def test_package_static_files(self):
        """Test that static files are accessible."""
        import jsoncrack_for_sphinx

        # Test that the package has static files directory
        static_dir = jsoncrack_for_sphinx.__path__[0] + "/static"
        import os

        assert os.path.exists(static_dir), "Static directory should exist"

        # Test that specific static files exist
        css_file = os.path.join(static_dir, "jsoncrack-schema.css")
        js_file = os.path.join(static_dir, "jsoncrack-sphinx.js")

        assert os.path.exists(css_file), "CSS file should exist"
        assert os.path.exists(js_file), "JavaScript file should exist"
