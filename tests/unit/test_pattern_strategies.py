"""Tests for pattern generation strategies."""

# Import all test classes for pytest discovery
from .pattern_strategies.test_join_functions import TestJoinWithSeparator
from .pattern_strategies.test_pattern_functions import (
    TestAddClassMethodPatterns,
    TestAddPackageNamePatterns,
    TestAddPathComponentPatterns,
    TestAddSlashSeparatedPatterns,
)
from .pattern_strategies.test_utility_functions import TestRemoveDuplicates

__all__ = [
    "TestJoinWithSeparator",
    "TestAddClassMethodPatterns",
    "TestAddPathComponentPatterns",
    "TestAddPackageNamePatterns",
    "TestAddSlashSeparatedPatterns",
    "TestRemoveDuplicates",
]
