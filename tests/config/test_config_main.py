"""
Main entry point for configuration tests.

This module imports all configuration test suites.
Individual test suites are organized in separate modules:
- test_config_classes.py: Basic configuration classes and enums
- test_config_parsing.py: Configuration parsing functionality
"""

# Import all test suites to ensure they are discovered by pytest
from .test_config_classes import (
    TestContainerConfig,
    TestDirections,
    TestRenderConfig,
    TestRenderMode,
    TestTheme,
)
from .test_config_parsing import (
    TestGetConfigValues,
    TestJsonCrackConfig,
    TestParseConfig,
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
