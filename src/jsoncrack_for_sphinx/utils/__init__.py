"""Utility functions and common types."""

# Import fixtures directly without going through other modules
from .fixtures import (
    create_function_schema,
    create_method_schema,
    create_option_schema,
)

# Export all public functions
__all__ = [
    "create_function_schema",
    "create_method_schema",
    "create_option_schema",
]


from typing import Any


def __getattr__(name: str) -> Any:
    """Lazy import for backward compatibility."""
    if name == "schema_to_rst":
        from ..generators.rst_generator import schema_to_rst

        return schema_to_rst
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
