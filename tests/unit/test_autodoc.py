"""
Tests for autodoc functionality.

This module imports all autodoc tests from submodules.
"""

from unit.autodoc.test_docstring_processing import TestAutodocProcessDocstring

# Import all test classes from submodules
from unit.autodoc.test_signature_processing import TestAutodocProcessSignature

# Expose test classes for pytest discovery
__all__ = [
    "TestAutodocProcessSignature",
    "TestAutodocProcessDocstring",
]
