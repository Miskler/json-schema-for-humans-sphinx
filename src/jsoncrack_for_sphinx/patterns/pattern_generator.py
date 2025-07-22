"""
Search pattern generation functionality.
"""

from typing import List, Tuple

from ..search.search_policy import SearchPolicy
from .pattern_strategies_impl import (
    add_class_method_patterns,
    add_package_name_patterns,
    add_path_component_patterns,
)
from .pattern_utils import process_custom_patterns, remove_duplicates


def generate_search_patterns(
    obj_name: str, search_policy: SearchPolicy
) -> List[Tuple[str, str]]:
    """
    Generate search patterns based on search policy.

    Args:
        obj_name: Full object name (e.g.,
            "perekrestok_api.endpoints.catalog.ProductService.similar")
        search_policy: Search policy configuration

    Returns:
        List of (pattern, file_type) tuples to try
    """
    patterns = []
    parts = obj_name.split(".")

    # Add custom patterns first (highest priority)
    patterns.extend(process_custom_patterns(parts, obj_name, search_policy))

    if len(parts) >= 2:
        # Strategy 1: Class.method only (most common case)
        patterns.extend(add_class_method_patterns(parts, search_policy))

        # Strategy 2: Path components based on include_path_to_file setting
        if search_policy.include_path_to_file and len(parts) >= 3:
            patterns.extend(add_path_component_patterns(parts, search_policy))

        # Strategy 3: Include package name if requested
        if search_policy.include_package_name:
            patterns.extend(add_package_name_patterns(parts, search_policy))

        # Strategy 4: Just method name
        method_name = parts[-1]
        patterns.extend(
            [
                (f"{method_name}.schema.json", "schema"),
                (f"{method_name}.json", "json"),
            ]
        )

    # Strategy 5: Full object name as is (fallback)
    patterns.extend(
        [
            (f"{obj_name}.schema.json", "schema"),
            (f"{obj_name}.json", "json"),
        ]
    )

    return remove_duplicates(patterns)
