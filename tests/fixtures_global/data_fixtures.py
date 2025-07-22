"""
Sample data fixtures for testing.
"""

import pytest


@pytest.fixture
def sample_schema():
    """Provide a sample JSON schema for testing."""
    return {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "title": "User",
        "description": "A user object with personal information",
        "properties": {
            "name": {
                "type": "string",
                "description": "The user's full name",
                "minLength": 1,
                "maxLength": 100,
            },
            "age": {
                "type": "integer",
                "minimum": 0,
                "maximum": 150,
                "description": "The user's age in years",
            },
            "email": {
                "type": "string",
                "format": "email",
                "description": "The user's email address",
            },
            "active": {
                "type": "boolean",
                "default": True,
                "description": "Whether the user account is active",
            },
        },
        "required": ["name", "email"],
        "additionalProperties": False,
    }


@pytest.fixture
def sample_json_data():
    """Provide sample JSON data for testing."""
    return {
        "id": 123,
        "name": "John Doe",
        "email": "john.doe@example.com",
        "age": 30,
        "active": True,
        "roles": ["user", "admin"],
        "profile": {
            "location": "San Francisco",
            "preferences": {"theme": "dark", "notifications": True},
        },
    }
