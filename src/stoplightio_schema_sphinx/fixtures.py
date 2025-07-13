"""
Pytest fixtures for testing the Sphinx extension.
"""

import json
import tempfile
from pathlib import Path
from typing import Dict, Any

import pytest

from .utils import schema_to_rst


@pytest.fixture
def temp_schema_dir():
    """Create a temporary directory for schema files."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


@pytest.fixture
def sample_schema():
    """Provide a sample JSON schema for testing."""
    return {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "title": "User",
        "description": "A user object",
        "properties": {
            "name": {
                "type": "string",
                "description": "The user's name"
            },
            "age": {
                "type": "integer",
                "minimum": 0,
                "description": "The user's age"
            },
            "email": {
                "type": "string",
                "format": "email",
                "description": "The user's email address"
            }
        },
        "required": ["name", "email"]
    }


@pytest.fixture
def schema_file(temp_schema_dir, sample_schema):
    """Create a sample schema file for testing."""
    schema_path = temp_schema_dir / "User.schema.json"
    with open(schema_path, 'w', encoding='utf-8') as f:
        json.dump(sample_schema, f, indent=2)
    return schema_path


@pytest.fixture
def schema_to_rst_fixture():
    """
    Fixture to convert schema files to reStructuredText.
    
    This fixture provides the schema_to_rst function for use in tests.
    """
    return schema_to_rst


# Helper functions for creating test schemas
def create_method_schema(temp_dir: Path, class_name: str, method_name: str, 
                        schema_data: Dict[str, Any]) -> Path:
    """Create a schema file for a method."""
    schema_path = temp_dir / f"{class_name}.{method_name}.schema.json"
    with open(schema_path, 'w', encoding='utf-8') as f:
        json.dump(schema_data, f, indent=2)
    return schema_path


def create_function_schema(temp_dir: Path, function_name: str, 
                          schema_data: Dict[str, Any]) -> Path:
    """Create a schema file for a function."""
    schema_path = temp_dir / f"{function_name}.schema.json"
    with open(schema_path, 'w', encoding='utf-8') as f:
        json.dump(schema_data, f, indent=2)
    return schema_path


def create_option_schema(temp_dir: Path, base_name: str, option_name: str,
                        schema_data: Dict[str, Any]) -> Path:
    """Create a schema file for an option."""
    schema_path = temp_dir / f"{base_name}.{option_name}.schema.json"
    with open(schema_path, 'w', encoding='utf-8') as f:
        json.dump(schema_data, f, indent=2)
    return schema_path
