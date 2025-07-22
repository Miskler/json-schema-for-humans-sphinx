"""
Main entry point for search policy tests.

Individual test suites are organized in separate modules:
- test_search_policy_core.py: PathSeparator and SearchPolicy core tests
- test_pattern_generation.py: Pattern generation functionality tests
- test_schema_finding.py: Schema file finding tests
- test_config_regression.py: Configuration integration and regression tests
"""

from .search_policy.test_config_regression import (
    TestConfigIntegration,
    TestRegressionCases,
    TestTargetCases,
)
from .search_policy.test_pattern_generation import TestGenerateSearchPatterns
from .search_policy.test_schema_finding import TestFindSchemaForObject

# Import all test suites to ensure they are discovered by pytest
from .search_policy.test_search_policy_core import (
    TestPathSeparator,
    TestSearchPolicy,
)

__all__ = [
    "TestPathSeparator",
    "TestSearchPolicy",
    "TestGenerateSearchPatterns",
    "TestFindSchemaForObject",
    "TestConfigIntegration",
    "TestRegressionCases",
    "TestTargetCases",
]
