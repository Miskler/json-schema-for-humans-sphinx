"""
Backward compatibility module for jsoncrack_for_sphinx.schema_finder

This module provides backward compatibility for old imports.
All functionality has been moved to schema.schema_finder.
"""

# Re-export everything from the new location
from .schema.schema_finder import find_schema_for_object

__all__ = ["find_schema_for_object"]
