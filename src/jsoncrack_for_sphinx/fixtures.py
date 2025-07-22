"""
Backward compatibility module for fixtures

This module provides backward compatibility for old imports.
All functionality has been moved to utils.fixtures.
"""

# Re-export everything from the new location
from .utils.fixtures import *

__all__ = [
    "create_function_schema",
    "create_method_schema", 
    "create_option_schema",
    "schema_to_rst",
]
