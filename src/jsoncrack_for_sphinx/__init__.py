"""
Sphinx extension for automatically adding JSON schemas to documentation.

This extension integrates with JSONCrack to generate beautiful
interactive visualizations of JSON schemas and automatically includes them in
Sphinx documentation based on function and method names.
"""

__version__ = "0.1.1"
__author__ = "Miskler"

# Import main modules for easy access
from . import config, fixtures, utils

# Backward compatibility imports
from .core import extension
from .core.extension import setup
from .schema import schema_finder

# Keep __all__ minimal for public API
__all__ = [
    "setup",
]
