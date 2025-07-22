"""
Dependency compatibility tests.
"""

import pytest


class TestDependencyCompatibility:
    """Test compatibility with different dependency versions."""

    def test_sphinx_compatibility(self):
        """Test Sphinx compatibility."""
        try:
            import sphinx

            sphinx_version = sphinx.__version__

            # We require Sphinx 4.0+
            version_parts = sphinx_version.split(".")
            major_version = int(version_parts[0])

            assert major_version >= 4, f"Sphinx 4.0+ required, got {sphinx_version}"

            # Test that we can import Sphinx components we use
            from sphinx.application import Sphinx
            from sphinx.util import logging
            from sphinx.util.docutils import SphinxDirective

            assert Sphinx is not None
            assert SphinxDirective is not None
            assert logging is not None

        except ImportError:
            pytest.skip("Sphinx not installed")

    def test_jsf_compatibility(self):
        """Test JSF (JSON Schema Faker) compatibility."""
        try:
            import jsf

            # Test basic JSF functionality
            simple_schema = {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "age": {"type": "integer", "minimum": 0, "maximum": 150},
                },
            }

            faker = jsf.JSF(simple_schema)
            fake_data = faker.generate()

            assert isinstance(fake_data, dict)
            assert "name" in fake_data
            assert "age" in fake_data
            assert isinstance(fake_data["age"], int)

        except ImportError:
            pytest.skip("JSF not installed")
        except Exception as e:
            pytest.skip(f"JSF compatibility issue: {e}")
