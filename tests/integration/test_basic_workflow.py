"""
Integration tests for basic workflow functionality.
"""

import json
from pathlib import Path

from jsoncrack_for_sphinx.schema.schema_finder import find_schema_for_object


class TestBasicWorkflow:
    """Integration tests for basic workflow functionality."""

    def test_full_workflow_with_autodoc(self, temp_dir):
        """Test the full workflow with autodoc integration."""
        # Create a mock Python module
        module_content = '''
"""Test module for integration testing."""

class User:
    """User management class."""

    def create(self, user_data):
        """
        Create a new user.

        Args:
            user_data: User data dictionary

        Returns:
            Created user information
        """
        return {"id": 1, "name": user_data["name"]}

    def update(self, user_id, update_data):
        """
        Update an existing user.

        Args:
            user_id: ID of the user to update
            update_data: Data to update

        Returns:
            Updated user information
        """
        return {"id": user_id, "updated": True}


def process_data(data, options=None):
    """
    Process input data.

    Args:
        data: Input data to process
        options: Processing options

    Returns:
        Processing results
    """
    return {"processed": len(data)}
'''

        # Create module file
        module_file = temp_dir / "test_module.py"
        with open(module_file, "w") as f:
            f.write(module_content)

        # Create schema directory
        schema_dir = temp_dir / "schemas"
        schema_dir.mkdir()

        # Create schema files
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
            "process_data.schema.json": {
                "$schema": "http://json-schema.org/draft-07/schema#",
                "type": "object",
                "title": "Process Data",
                "properties": {
                    "data": {"type": "array"},
                    "options": {"type": "object"},
                },
            },
        }

        for filename, content in schemas.items():
            with open(schema_dir / filename, "w") as f:
                json.dump(content, f, indent=2)

        # Test finding schemas for objects
        assert (
            find_schema_for_object("test_module.User.create", str(schema_dir))
            is not None
        )
        assert (
            find_schema_for_object("test_module.User.update", str(schema_dir))
            is not None
        )
        assert (
            find_schema_for_object("test_module.process_data", str(schema_dir))
            is not None
        )

        # Test that schemas are found correctly
        schema_result = find_schema_for_object(
            "test_module.User.create", str(schema_dir)
        )
        assert schema_result is not None
        schema_path, file_type = schema_result
        assert Path(schema_path).name == "User.create.schema.json"
        assert file_type == "schema"
