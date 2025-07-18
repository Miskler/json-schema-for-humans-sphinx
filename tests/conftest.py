"""
Pytest configuration and fixtures for the jsoncrack-for-sphinx extension.
"""

import json
import tempfile
from pathlib import Path
from typing import Any, Dict
from unittest.mock import Mock

import pytest

# Import the function we need for the fixture
from jsoncrack_for_sphinx.utils import schema_to_rst


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


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


@pytest.fixture
def mock_sphinx_app():
    """Create a mock Sphinx application for testing."""
    app = Mock()
    app.config = Mock()
    app.env = Mock()
    app.env.config = app.config

    # Default config values
    app.config.json_schema_dir = None
    app.config.jsoncrack_render_mode = "onclick"
    app.config.jsoncrack_theme = None
    app.config.jsoncrack_direction = "RIGHT"
    app.config.jsoncrack_height = "500"
    app.config.jsoncrack_width = "100%"
    app.config.jsoncrack_onscreen_threshold = 0.1
    app.config.jsoncrack_onscreen_margin = "50px"
    app.config.html_static_path = []

    # Mock methods
    app.add_config_value = Mock()
    app.add_directive = Mock()
    app.connect = Mock()
    app.add_css_file = Mock()
    app.add_js_file = Mock()

    return app


@pytest.fixture
def mock_sphinx_env():
    """Create a mock Sphinx environment for testing."""
    env = Mock()
    env.config = Mock()
    env.config.json_schema_dir = None
    return env


@pytest.fixture
def mock_directive_args():
    """Create mock arguments for directive testing."""
    return {
        "arguments": ["User.create"],
        "options": {
            "title": "Test Schema",
            "description": "Test description",
            "render_mode": "onclick",
            "direction": "RIGHT",
            "height": "500",
        },
        "content": [],
        "content_offset": 0,
        "block_text": "",
        "state": Mock(),
        "state_machine": Mock(),
    }


def create_test_schema_file(
    temp_dir: Path, filename: str, schema_data: Dict[str, Any]
) -> Path:
    """Helper function to create a test schema file."""
    schema_path = temp_dir / filename
    with open(schema_path, "w", encoding="utf-8") as f:
        json.dump(schema_data, f, indent=2)
    return schema_path


def create_test_json_file(
    temp_dir: Path, filename: str, json_data: Dict[str, Any]
) -> Path:
    """Helper function to create a test JSON file."""
    json_path = temp_dir / filename
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=2)
    return json_path


@pytest.fixture
def schema_to_rst_fixture():
    """
    Fixture to convert schema files to reStructuredText.

    This fixture provides the schema_to_rst function for use in tests.
    """
    return schema_to_rst
