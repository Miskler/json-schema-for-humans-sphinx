"""
RST generation utilities for JSON schemas.
"""

import json
from pathlib import Path
from typing import Any, Dict, Optional


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
        # Read and validate JSON schema
        with open(schema_path, "r", encoding="utf-8") as f:
            schema_data = json.load(f)

        # Create simple HTML representation of schema
        html_content = _generate_simple_schema_html(schema_data)

        # Convert to RST
        rst_lines = []

        if title:
            rst_lines.extend(
                [
                    title,
                    "=" * len(title),
                    "",
                ]
            )

        rst_lines.extend(
            [
                ".. raw:: html",
                "",
                '   <div class="json-schema-container">',
                f"   {html_content}",
                "   </div>",
                "",
            ]
        )

        return "\n".join(rst_lines)

    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in schema file {schema_path}: {e}")
    except Exception as e:
        raise RuntimeError(f"Error processing schema file {schema_path}: {e}")


def _generate_simple_schema_html(schema_data: Dict[str, Any]) -> str:
    """
    Generate simple HTML representation of a JSON schema.

    Args:
        schema_data: JSON schema data

    Returns:
        HTML string representing the schema
    """
    html_parts = []

    # Add title if present
    if "title" in schema_data:
        html_parts.append(f'<h3>{schema_data["title"]}</h3>')

    # Add description if present
    if "description" in schema_data:
        html_parts.append(f'<p>{schema_data["description"]}</p>')

    # Add basic schema info
    html_parts.append('<div class="schema-info">')

    if "type" in schema_data:
        html_parts.append(f'<p><strong>Type:</strong> {schema_data["type"]}</p>')

    # Add properties if it's an object schema
    if schema_data.get("type") == "object" and "properties" in schema_data:
        html_parts.append("<h4>Properties:</h4>")
        html_parts.append("<ul>")
        for prop_name, prop_info in schema_data["properties"].items():
            prop_type = prop_info.get("type", "unknown")
            prop_desc = prop_info.get("description", "")
            is_required = prop_name in schema_data.get("required", [])
            required_text = " (required)" if is_required else ""

            prop_line = (
                f"<li><strong>{prop_name}</strong> " f"({prop_type}){required_text}"
            )
            html_parts.append(prop_line)
            if prop_desc:
                html_parts.append(f"<br>{prop_desc}")
            html_parts.append("</li>")
        html_parts.append("</ul>")

    # Add raw schema as collapsible section
    html_parts.append("<details>")
    html_parts.append("<summary>Raw Schema</summary>")
    html_parts.append("<pre>")
    html_parts.append(json.dumps(schema_data, indent=2))
    html_parts.append("</pre>")
    html_parts.append("</details>")

    html_parts.append("</div>")

    return "\n".join(html_parts)
