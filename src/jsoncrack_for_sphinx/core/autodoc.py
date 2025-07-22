"""
Autodoc integration for automatic schema inclusion.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from sphinx.application import Sphinx
from sphinx.util import logging

from ..config.config_utils import get_jsoncrack_config
from ..generators.html_generator import generate_schema_html
from ..schema.schema_finder import find_schema_for_object

logger = logging.getLogger(__name__)


def autodoc_process_signature(
    app: Sphinx,
    what: str,
    name: str,
    obj: Any,
    options: Dict[str, Any],
    signature: str,
    return_annotation: str,
) -> Optional[Tuple[str, str]]:
    """Process autodoc signatures and add schema information."""
    logger.debug(f"Processing signature for {what}: {name}")

    # Get configuration
    jsoncrack_config = get_jsoncrack_config(app.config)

    # Check if autodoc is disabled
    if jsoncrack_config.disable_autodoc:
        logger.debug("Autodoc is disabled in configuration")
        return None

    # Check if this object should be ignored
    for ignore_pattern in jsoncrack_config.autodoc_ignore:
        if name.startswith(ignore_pattern):
            logger.debug(f"Ignoring {name} due to pattern: {ignore_pattern}")
            return None

    if what not in ("function", "method", "class"):
        logger.debug(f"Skipping {what} (not function/method/class)")
        return None

    config = app.config
    schema_dir = getattr(config, "json_schema_dir", None)

    if not schema_dir:
        logger.debug("No json_schema_dir configured, skipping schema search")
        return None

    logger.debug(f"Searching for schema for {name} in {schema_dir}")

    # Get search policy from configuration
    search_policy = jsoncrack_config.search_policy
    logger.debug(f"Using search policy from config: {search_policy}")

    # Find schema file
    schema_result = find_schema_for_object(name, schema_dir, search_policy)
    if not schema_result:
        logger.debug(f"No schema found for {name}")
        return None

    schema_path, file_type = schema_result
    logger.info(f"Found schema for {name}: {schema_path} (type: {file_type})")

    # Store schema path and type to be used later
    if not hasattr(app.env, "_jsoncrack_schema_paths"):
        setattr(app.env, "_jsoncrack_schema_paths", {})

    schema_paths = getattr(app.env, "_jsoncrack_schema_paths")
    schema_paths[name] = (str(schema_path), file_type)
    logger.debug(f"Stored schema path for {name}")

    return None


def autodoc_process_docstring(
    app: Sphinx,
    what: str,
    name: str,
    obj: Any,
    options: Dict[str, Any],
    lines: List[str],
) -> None:
    """Process docstrings and add schema HTML."""
    logger.debug(f"Processing docstring for {what}: {name}")

    # Get configuration
    jsoncrack_config = get_jsoncrack_config(app.config)

    # Check if autodoc is disabled
    if jsoncrack_config.disable_autodoc:
        logger.debug("Autodoc is disabled in configuration")
        return

    # Check if this object should be ignored
    for ignore_pattern in jsoncrack_config.autodoc_ignore:
        if name.startswith(ignore_pattern):
            logger.debug(f"Ignoring {name} due to pattern: {ignore_pattern}")
            return

    if what not in ("function", "method", "class"):
        logger.debug(f"Skipping {what} (not function/method/class)")
        return

    if not hasattr(app.env, "_jsoncrack_schema_paths"):
        logger.debug("No schema paths stored, skipping")
        return

    schema_paths = getattr(app.env, "_jsoncrack_schema_paths")
    schema_data = schema_paths.get(name)
    if not schema_data:
        logger.debug(f"No schema data found for {name}")
        return

    logger.debug(f"Processing schema for {name}: {schema_data}")

    if isinstance(schema_data, str):
        # Backward compatibility: if it's just a string, assume it's a schema file
        schema_path_str = schema_data
        file_type = "schema"
    else:
        schema_path_str, file_type = schema_data

    schema_path = Path(schema_path_str)

    if not schema_path.exists():
        logger.error(f"Schema file does not exist: {schema_path}")
        return

    logger.info(f"Adding schema to docstring for {name}: {schema_path}")

    # Generate schema HTML
    try:
        html_content = generate_schema_html(schema_path, file_type, app.config)
        logger.debug(f"Generated HTML content for {name} (length: {len(html_content)})")
    except Exception as e:
        logger.error(f"Error generating schema HTML for {name}: {e}")
        return

    # Add schema HTML to docstring
    lines.extend(
        [
            "",
            ".. raw:: html",
            "",
            f"   {html_content}",
            "",
        ]
    )
    logger.debug(f"Added schema HTML to docstring for {name}")
