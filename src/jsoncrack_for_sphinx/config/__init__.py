"""Configuration management for JSONCrack Sphinx extension."""

# Import all configuration components from submodules
from ..search.search_policy import SearchPolicy
from ..utils.types import Directions, PathSeparator, RenderMode, Theme
from .config_classes import ContainerConfig, RenderConfig
from .config_parser import JsonCrackConfig, get_config_values, parse_config

# Export all public classes and functions
__all__ = [
    # Types and enums
    "RenderMode",
    "Directions",
    "Theme",
    "PathSeparator",
    # Configuration classes
    "ContainerConfig",
    "RenderConfig",
    "SearchPolicy",
    "JsonCrackConfig",
    # Utility functions
    "parse_config",
    "get_config_values",
]
