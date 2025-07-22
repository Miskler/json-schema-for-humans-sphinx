"""
Backward compatibility module for jsoncrack_for_sphinx.extension

This module provides backward compatibility for old imports.
All functionality has been moved to core.extension.
"""

# Re-export everything from the new location
from .core.extension import setup

__all__ = ["setup"]
