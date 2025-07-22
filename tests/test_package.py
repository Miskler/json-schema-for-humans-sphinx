"""
Tests for the main package.

This module imports all package tests from separate modules.
"""

from .package.test_package_compatibility import TestPackageCompatibility
from .package.test_package_imports import TestPackageImports
from .package.test_package_integration import TestPackageIntegration

# Import all test classes from separated modules
from .package.test_package_metadata import TestPackageMetadata

# Re-export test classes for pytest discovery
__all__ = [
    "TestPackageMetadata",
    "TestPackageImports",
    "TestPackageIntegration",
    "TestPackageCompatibility",
]
