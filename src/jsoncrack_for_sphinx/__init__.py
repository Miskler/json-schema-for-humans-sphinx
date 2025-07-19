"""
Sphinx extension for automatically adding JSON schemas to documentation.

This extension integrates with JSONCrack to generate beautiful
interactive visualizations of JSON schemas and automatically includes them in
Sphinx documentation based on function and method names.
"""

__version__ = "0.1.0"
__author__ = "Miskler"

from .extension import setup

__all__ = [
    "setup"
]
