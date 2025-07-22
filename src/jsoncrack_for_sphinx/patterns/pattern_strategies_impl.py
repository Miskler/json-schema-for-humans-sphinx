"""
Pattern generation strategies for different use cases.
"""

from typing import TYPE_CHECKING, List, Tuple

from .pattern_utils import join_with_separator

if TYPE_CHECKING:
    from ..search.search_policy import SearchPolicy


def add_class_method_patterns(
    parts: List[str], search_policy: "SearchPolicy"
) -> List[Tuple[str, str]]:
    """Add class.method patterns."""
    class_method_parts = parts[-2:]  # Last 2 parts
    class_method = join_with_separator(
        class_method_parts, search_policy.path_to_class_separator
    )
    return [
        (f"{class_method}.schema.json", "schema"),
        (f"{class_method}.json", "json"),
    ]


def add_path_component_patterns(
    parts: List[str], search_policy: "SearchPolicy"
) -> List[Tuple[str, str]]:
    """Add intermediate path component patterns."""
    patterns = []

    # Generate intermediate patterns like "catalog.ProductService.similar"
    for i in range(len(parts) - 3, 0, -1):
        partial_parts = parts[i:]
        if len(partial_parts) >= 3:
            partial_path = join_with_separator(
                partial_parts, search_policy.path_to_file_separator
            )
            patterns.extend(
                [
                    (f"{partial_path}.schema.json", "schema"),
                    (f"{partial_path}.json", "json"),
                ]
            )

    # Include intermediate path components without package name
    if not search_policy.include_package_name and len(parts) >= 3:
        without_package = parts[1:]
        if search_policy.path_to_file_separator.name == "SLASH":
            patterns.extend(
                add_slash_separated_patterns(without_package, search_policy)
            )
        else:
            full_path = join_with_separator(
                without_package, search_policy.path_to_file_separator
            )
            patterns.extend(
                [
                    (f"{full_path}.schema.json", "schema"),
                    (f"{full_path}.json", "json"),
                ]
            )

    return patterns


def add_package_name_patterns(
    parts: List[str], search_policy: "SearchPolicy"
) -> List[Tuple[str, str]]:
    """Add patterns that include package name."""
    patterns = []

    if search_policy.path_to_file_separator.name == "SLASH":
        if len(parts) >= 2:
            dir_parts = parts[:-2]
            class_method_parts = parts[-2:]
            class_method = join_with_separator(
                class_method_parts, search_policy.path_to_class_separator
            )
            if dir_parts:
                dir_path = "/".join(dir_parts)
                patterns.extend(
                    [
                        (f"{dir_path}/{class_method}.schema.json", "schema"),
                        (f"{dir_path}/{class_method}.json", "json"),
                    ]
                )
    else:
        full_path = join_with_separator(parts, search_policy.path_to_file_separator)
        patterns.extend(
            [
                (f"{full_path}.schema.json", "schema"),
                (f"{full_path}.json", "json"),
            ]
        )

    return patterns


def add_slash_separated_patterns(
    without_package: List[str], search_policy: "SearchPolicy"
) -> List[Tuple[str, str]]:
    """Add patterns for slash-separated directory structure."""
    patterns = []

    if len(without_package) >= 2:
        dir_parts = without_package[:-2]
        class_method_parts = without_package[-2:]
        class_method = join_with_separator(
            class_method_parts, search_policy.path_to_class_separator
        )
        if dir_parts:
            dir_path = "/".join(dir_parts)
            patterns.extend(
                [
                    (f"{dir_path}/{class_method}.schema.json", "schema"),
                    (f"{dir_path}/{class_method}.json", "json"),
                ]
            )

    return patterns
