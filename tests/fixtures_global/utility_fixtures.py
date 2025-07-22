"""
Utility fixtures for testing.
"""

import pytest

# Import the function we need for the fixture directly from generators
from jsoncrack_for_sphinx.generators.rst_generator import schema_to_rst


@pytest.fixture
def schema_to_rst_fixture():
    """
    Fixture to convert schema files to reStructuredText.

    This fixture provides the schema_to_rst function for use in tests.
    """
    return schema_to_rst
