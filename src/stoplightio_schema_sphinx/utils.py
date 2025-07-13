"""
Utility functions for working with JSON schemas and fixtures.
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from json_schema_for_humans import generate
from json_schema_for_humans.generation_configuration import GenerationConfiguration


def schema_to_rst(schema_path: Path, title: Optional[str] = None) -> str:
    """
    Convert a JSON schema file to reStructuredText format.
    
    This function is provided as a fixture for tests to convert schema
    files to reStructuredText format.
    
    Args:
        schema_path: Path to the JSON schema file
        title: Optional title for the schema section
        
    Returns:
        reStructuredText representation of the schema
    """
    if not schema_path.exists():
        raise FileNotFoundError(f"Schema file not found: {schema_path}")
    
    try:
        # Generate HTML first
        config = GenerationConfiguration(
            minify=False,
            deprecated_from_description=True,
            default_from_description=True,
            expand_buttons=True,
            copy_css=False,
            copy_js=False,
            template_name="js",
        )
        
        html_content = generate.generate_from_schema(
            schema_file=schema_path,
            config=config
        )
        
        # Convert to RST
        rst_lines = []
        
        if title:
            rst_lines.extend([
                title,
                "=" * len(title),
                "",
            ])
        
        rst_lines.extend([
            ".. raw:: html",
            "",
            f"   <div class=\"json-schema-container\">",
            f"   {html_content}",
            f"   </div>",
            "",
        ])
        
        return "\n".join(rst_lines)
        
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in schema file {schema_path}: {e}")
    except Exception as e:
        raise RuntimeError(f"Error processing schema file {schema_path}: {e}")


def validate_schema_file(schema_path: Path) -> bool:
    """
    Validate that a schema file contains valid JSON.
    
    Args:
        schema_path: Path to the schema file
        
    Returns:
        True if the file contains valid JSON, False otherwise
    """
    try:
        with open(schema_path, 'r', encoding='utf-8') as f:
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
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema_data = json.load(f)
        
        info = {
            'file_name': schema_path.name,
            'title': schema_data.get('title', ''),
            'description': schema_data.get('description', ''),
            'type': schema_data.get('type', ''),
            'properties': list(schema_data.get('properties', {}).keys()),
            'required': schema_data.get('required', []),
        }
        
        return info
        
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in schema file {schema_path}: {e}")
    except Exception as e:
        raise RuntimeError(f"Error reading schema file {schema_path}: {e}")


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
            rst_lines.extend([
                f"**{info['file_name']}**",
                "",
                f"   :Title: {info['title']}",
                f"   :Type: {info['type']}",
                f"   :Properties: {', '.join(info['properties'])}",
                "",
            ])
        except Exception as e:
            rst_lines.extend([
                f"**{schema_file.name}** (Error: {e})",
                "",
            ])
    
    return "\n".join(rst_lines)
