"""
Schema file utilities and validation.
"""

import json
from pathlib import Path
from typing import Any, Dict, List


def validate_schema_file(schema_path: Path) -> bool:
    """
    Validate that a schema file contains valid JSON.

    Args:
        schema_path: Path to the schema file

    Returns:
        True if the file contains valid JSON, False otherwise
    """
    try:
        with open(schema_path, "r", encoding="utf-8") as f:
            json.load(f)
        return True
    except (json.JSONDecodeError, FileNotFoundError):
        return False


def find_schema_files(schema_dir: Path, pattern: str = "*.schema.json") -> List[Path]:
    """
    Find all schema files in a directory matching a pattern.

    Args:
        schema_dir: Directory to search for schema files
        pattern: Glob pattern to match schema files

    Returns:
        List of paths to schema files
    """
    if not schema_dir.exists():
        return []

    return list(schema_dir.glob(pattern))


def get_schema_info(schema_path: Path) -> Dict[str, Any]:
    """
    Extract basic information from a schema file.

    Args:
        schema_path: Path to the schema file

    Returns:
        Dictionary containing schema information
    """
    if not schema_path.exists():
        raise FileNotFoundError(f"Schema file not found: {schema_path}")

    try:
        with open(schema_path, "r", encoding="utf-8") as f:
            schema_data = json.load(f)

        info = {
            "file_name": schema_path.name,
            "title": schema_data.get("title", ""),
            "description": schema_data.get("description", ""),
            "type": schema_data.get("type", ""),
            "properties": list(schema_data.get("properties", {}).keys()),
            "required": schema_data.get("required", []),
        }

        return info

    except json.JSONDecodeError:
        # Return default values for invalid JSON
        return {
            "file_name": schema_path.name,
            "title": "",
            "description": "",
            "type": "",
            "properties": [],
            "required": [],
        }
    except Exception:
        # Return default values for other errors
        return {
            "file_name": schema_path.name,
            "title": "",
            "description": "",
            "type": "",
            "properties": [],
            "required": [],
        }


def create_schema_index(schema_dir: Path) -> str:
    """
    Create an index of all schema files in a directory.

    Args:
        schema_dir: Directory containing schema files

    Returns:
        reStructuredText index of all schemas
    """
    schema_files = find_schema_files(schema_dir)

    if not schema_files:
        return "No schema files found."

    rst_lines = [
        "Schema Index",
        "============",
        "",
    ]

    for schema_file in sorted(schema_files):
        try:
            info = get_schema_info(schema_file)
            rst_lines.extend(
                [
                    f"**{info['file_name']}**",
                    "",
                    f"   :Title: {info['title']}",
                    f"   :Type: {info['type']}",
                    f"   :Properties: {', '.join(info['properties'])}",
                    "",
                ]
            )
        except Exception as e:
            rst_lines.extend(
                [
                    f"**{schema_file.name}** (Error: {e})",
                    "",
                ]
            )

    return "\n".join(rst_lines)
