"""
Entry point for pattern strategies tests.
"""

# Import all test classes for pytest discovery
from .test_join_functions import TestJoinWithSeparator
from .test_pattern_functions import (
    TestAddClassMethodPatterns,
    TestAddPackageNamePatterns,
    TestAddPathComponentPatterns,
    TestAddSlashSeparatedPatterns,
)
from .test_utility_functions import TestRemoveDuplicates

__all__ = [
    "TestJoinWithSeparator",
    "TestAddClassMethodPatterns",
    "TestAddPathComponentPatterns",
    "TestAddPackageNamePatterns",
    "TestAddSlashSeparatedPatterns",
    "TestRemoveDuplicates",
]
