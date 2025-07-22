"""
Main entry point for configuration tests.

This module imports all configuration test suites.
Individual test suites are organized in separate modules:
- test_config_classes.py: Basic configuration classes and enums
- test_config_parsing.py: Configuration parsing functionality
"""

# Import all test suites to ensure they are discovered by pytest
from .test_config_classes import (
    TestRenderMode,
    TestDirections,
    TestTheme,
    TestContainerConfig,
    TestRenderConfig,
)
from .test_config_parsing import (
    TestJsonCrackConfig,
    TestParseConfig,
    TestGetConfigValues,
)

__all__ = [
    "TestRenderMode",
    "TestDirections",
    "TestTheme",
    "TestContainerConfig",
    "TestRenderConfig",
    "TestJsonCrackConfig",
    "TestParseConfig",
    "TestGetConfigValues",
]
