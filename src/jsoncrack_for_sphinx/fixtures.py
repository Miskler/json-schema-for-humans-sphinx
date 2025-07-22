"""
Backward compatibility module for fixtures

This module provides backward compatibility for old imports.
All functionality has been moved to utils.fixtures.
"""

from .generators.rst_generator import schema_to_rst

# Re-export everything from the new location
from .utils.fixtures import (
    create_function_schema,
    create_method_schema,
    create_option_schema,
)

__all__ = [
    "create_function_schema",
    "create_method_schema",
    "create_option_schema",
    "schema_to_rst",
]
