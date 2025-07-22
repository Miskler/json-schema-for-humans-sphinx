"""
Utility functions for pattern generation.
"""

from typing import TYPE_CHECKING, List, Tuple

from ..utils.types import PathSeparator

if TYPE_CHECKING:
    from ..search.search_policy import SearchPolicy


def join_with_separator(parts_list: List[str], separator: PathSeparator) -> str:
    """Join parts with the specified separator."""
    if separator == PathSeparator.DOT:
        return ".".join(parts_list)
    elif separator == PathSeparator.SLASH:
        return "/".join(parts_list)
    elif separator == PathSeparator.NONE:
        return "".join(parts_list)
    else:
        return ".".join(parts_list)  # fallback


def remove_duplicates(patterns: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
    """Remove duplicate patterns while preserving order."""
    seen = set()
    unique_patterns = []
    for pattern, file_type in patterns:
        key = (pattern, file_type)
        if key not in seen:
            seen.add(key)
            unique_patterns.append((pattern, file_type))
    return unique_patterns


def process_custom_patterns(
    parts: List[str], obj_name: str, search_policy: "SearchPolicy"
) -> List[Tuple[str, str]]:
    """Process custom patterns with placeholder substitution."""
    patterns = []

    for custom_pattern in search_policy.custom_patterns:
        # Substitute placeholders in custom patterns
        expanded_pattern = custom_pattern
        if len(parts) >= 2:
            class_name = parts[-2]  # Second to last part
            method_name = parts[-1]  # Last part
            expanded_pattern = expanded_pattern.replace("{class_name}", class_name)
            expanded_pattern = expanded_pattern.replace("{method_name}", method_name)
        expanded_pattern = expanded_pattern.replace("{object_name}", obj_name)

        # Check if pattern already has file extension
        if expanded_pattern.endswith((".json", ".schema.json")):
            # Pattern already includes extension, add as-is
            if expanded_pattern.endswith(".schema.json"):
                patterns.append((expanded_pattern, "schema"))
            else:
                patterns.append((expanded_pattern, "json"))
        else:
            # Pattern doesn't have extension, add both variants
            patterns.extend(
                [
                    (f"{expanded_pattern}.schema.json", "schema"),
                    (f"{expanded_pattern}.json", "json"),
                ]
            )

    return patterns
