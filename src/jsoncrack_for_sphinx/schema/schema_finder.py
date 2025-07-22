"""
Schema file search functionality.
"""

from pathlib import Path
from typing import Optional, Tuple

from sphinx.util import logging

from ..patterns.pattern_generator import generate_search_patterns
from ..search.search_policy import SearchPolicy

logger = logging.getLogger(__name__)


def find_schema_for_object(
    obj_name: str, schema_dir: str, search_policy: Optional[SearchPolicy] = None
) -> Optional[Tuple[Path, str]]:
    """
    Find schema file for a given object (function/method).

    Args:
        obj_name: Full name of the object (e.g., "example_module.User.create")
        schema_dir: Directory containing schema files
        search_policy: Search policy to use (optional, uses default if None)

    Returns:
        Tuple of (Path to schema file, file type) if found, None otherwise
        File type is either 'schema' for .schema.json files or 'json' for .json files
    """
    logger.debug(f"Looking for schema for object: {obj_name}")
    logger.debug(f"Schema directory: {schema_dir}")

    if not schema_dir:
        logger.debug("No schema directory configured")
        return None

    schema_dir_path = Path(schema_dir)
    if not schema_dir_path.exists():
        logger.warning(f"Schema directory does not exist: {schema_dir}")
        return None

    # Use default search policy if none provided
    if search_policy is None:
        search_policy = SearchPolicy()
        logger.debug("Using default search policy")
    else:
        logger.debug(f"Using custom search policy: {search_policy}")

    # Generate search patterns using the policy
    patterns = generate_search_patterns(obj_name, search_policy)

    logger.debug(f"Trying {len(patterns)} patterns:")
    for pattern, file_type in patterns:
        logger.debug(f"  Checking pattern: {pattern}")
        schema_path = schema_dir_path / pattern
        if schema_path.exists():
            logger.info(
                f"Found schema file: {schema_path} (type: {file_type}) "
                f"for object: {obj_name}"
            )
            return schema_path, file_type
        else:
            logger.debug(f"    File not found: {schema_path}")

    logger.warning(f"No schema file found for object: {obj_name}")
    return None
