"""
Main entry point for utils tests.

This module imports all utils test suites.
Individual test suites are organized in separate modules:
- test_schema_to_rst.py: Schema to RST conversion tests
- test_schema_validation.py: Schema file validation tests
- test_schema_utils.py: Schema file finding and info extraction tests
"""

# Import all test suites to ensure they are discovered by pytest
from .test_schema_to_rst import TestSchemaToRst
from .test_schema_utils import TestFindSchemaFiles, TestGetSchemaInfo
from .test_schema_validation import TestValidateSchemaFile

__all__ = [
    "TestSchemaToRst",
    "TestValidateSchemaFile",
    "TestFindSchemaFiles",
    "TestGetSchemaInfo",
]
