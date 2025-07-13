"""
Conftest for pytest.
"""

import json
import tempfile
from pathlib import Path

import pytest


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
def complex_schema():
    """Provide a more complex JSON schema for testing."""
    return {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "title": "API Response",
        "description": "Response from API endpoint",
        "properties": {
            "status": {
                "type": "string",
                "enum": ["success", "error"],
                "description": "Response status"
            },
            "data": {
                "type": "object",
                "properties": {
                    "users": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {
                                    "type": "integer",
                                    "description": "User ID"
                                },
                                "name": {
                                    "type": "string",
                                    "description": "User name"
                                },
                                "active": {
                                    "type": "boolean",
                                    "default": True,
                                    "description": "Whether user is active"
                                }
                            },
                            "required": ["id", "name"]
                        }
                    },
                    "total": {
                        "type": "integer",
                        "minimum": 0,
                        "description": "Total number of users"
                    }
                },
                "required": ["users", "total"]
            },
            "error": {
                "type": "object",
                "properties": {
                    "code": {
                        "type": "integer",
                        "description": "Error code"
                    },
                    "message": {
                        "type": "string",
                        "description": "Error message"
                    }
                }
            }
        },
        "required": ["status"],
        "oneOf": [
            {
                "properties": {
                    "status": {"const": "success"}
                },
                "required": ["data"]
            },
            {
                "properties": {
                    "status": {"const": "error"}
                },
                "required": ["error"]
            }
        ]
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
    from stoplightio_schema_sphinx.utils import schema_to_rst
    return schema_to_rst
