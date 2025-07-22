"""
File-based fixtures for testing.
"""

import json

import pytest


@pytest.fixture
def schema_file(temp_dir, sample_schema):
    """Create a sample schema file for testing."""
    schema_path = temp_dir / "User.schema.json"
    with open(schema_path, "w", encoding="utf-8") as f:
        json.dump(sample_schema, f, indent=2)
    return schema_path


@pytest.fixture
def json_file(temp_dir, sample_json_data):
    """Create a sample JSON file for testing."""
    json_path = temp_dir / "User.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(sample_json_data, f, indent=2)
    return json_path


@pytest.fixture
def schema_dir(temp_dir):
    """Create a directory with multiple schema files for testing."""
    # Create various schema files to test different patterns
    schemas = {
        "User.create.schema.json": {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "title": "User Creation",
            "properties": {
                "name": {"type": "string"},
                "email": {"type": "string", "format": "email"},
            },
            "required": ["name", "email"],
        },
        "User.update.schema.json": {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "title": "User Update",
            "properties": {"name": {"type": "string"}, "age": {"type": "integer"}},
        },
        "User.example.json": {
            "name": "John Doe",
            "email": "john@example.com",
            "age": 30,
        },
        "process_data.schema.json": {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "title": "Process Data",
            "properties": {"input": {"type": "array"}, "options": {"type": "object"}},
        },
        "invalid.schema.json": "invalid json content",
    }

    for filename, content in schemas.items():
        file_path = temp_dir / filename
        with open(file_path, "w", encoding="utf-8") as f:
            if isinstance(content, dict):
                json.dump(content, f, indent=2)
            else:
                f.write(content)

    return temp_dir
