"""
Basic fixtures for temporary directories and file handling.
"""

import json
import tempfile
from pathlib import Path
from typing import Any, Dict

import pytest


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


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
