"""
Compatibility tests for different Python versions and dependencies.

This module imports all compatibility tests from submodules.
"""

from .compatibility.test_backward_compatibility import TestBackwardCompatibility
from .compatibility.test_dependency_compatibility import TestDependencyCompatibility
from .compatibility.test_feature_compatibility import TestFeatureCompatibility

# Import all test classes from submodules
from .compatibility.test_python_compatibility import TestPythonCompatibility

# Expose test classes for pytest discovery
__all__ = [
    "TestPythonCompatibility",
    "TestDependencyCompatibility",
    "TestBackwardCompatibility",
    "TestFeatureCompatibility",
]
