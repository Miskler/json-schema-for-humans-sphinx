"""
Tests for package metadata and version information.
"""

import jsoncrack_for_sphinx


class TestPackageMetadata:
    """Test package metadata."""

    def test_package_metadata(self):
        """Test package metadata."""
        assert hasattr(jsoncrack_for_sphinx, "__version__")
        assert hasattr(jsoncrack_for_sphinx, "__author__")
        assert jsoncrack_for_sphinx.__author__ == "Miskler"

    def test_package_version_consistency(self):
        """Test that package version is consistent."""

        # Test that the version is a string
        assert isinstance(jsoncrack_for_sphinx.__version__, str)

        # Test that the version follows semantic versioning
        version_parts = jsoncrack_for_sphinx.__version__.split(".")
        assert len(version_parts) >= 2  # At least major.minor
        # major and minor are digits
        assert all(part.isdigit() for part in version_parts[:2])

    def test_package_documentation(self):
        """Test that package has documentation."""
        # Test that the module has a docstring
        assert jsoncrack_for_sphinx.__doc__ is not None
        assert len(jsoncrack_for_sphinx.__doc__.strip()) > 0

        # Test that setup function has documentation
        from jsoncrack_for_sphinx import setup

        assert setup.__doc__ is not None
        assert len(setup.__doc__.strip()) > 0
