"""
Custom pattern processing utilities.
"""

from typing import List, Tuple

from ..search.search_policy import SearchPolicy


def process_custom_patterns(
    parts: List[str], obj_name: str, search_policy: SearchPolicy
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
