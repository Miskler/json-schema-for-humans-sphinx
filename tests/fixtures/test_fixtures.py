"""
Tests for the fixtures module.

This module imports all fixture tests from submodules.
"""

from .fixtures_tests.test_complex_scenarios import TestComplexScenarios

# Import all test classes from submodules
from .fixtures_tests.test_fixture_functions import TestFixtures
from .fixtures_tests.test_helper_functions import TestHelperFunctions

# Expose test classes for pytest discovery
__all__ = [
    "TestFixtures",
    "TestHelperFunctions",
    "TestComplexScenarios",
]
