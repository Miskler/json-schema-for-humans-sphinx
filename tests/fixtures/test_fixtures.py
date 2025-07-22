"""
Tests for the fixtures module.

This module imports all fixture tests from submodules.
"""

# Import all test classes from submodules
from fixtures.fixtures_tests.test_fixture_functions import TestFixtures
from fixtures.fixtures_tests.test_helper_functions import TestHelperFunctions
from fixtures.fixtures_tests.test_complex_scenarios import TestComplexScenarios

# Expose test classes for pytest discovery
__all__ = [
    "TestFixtures",
    "TestHelperFunctions",
    "TestComplexScenarios",
]
