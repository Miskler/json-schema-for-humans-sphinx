"""
Search policy configuration for schema files.
"""

from typing import Optional

from ..utils.types import PathSeparator


class SearchPolicy:
    """Schema file search policy configuration."""

    def __init__(
        self,
        include_package_name: bool = False,
        include_path_to_file: bool = True,
        path_to_file_separator: PathSeparator = PathSeparator.DOT,
        path_to_class_separator: PathSeparator = PathSeparator.DOT,
        custom_patterns: Optional[list] = None,
    ):
        """
        Configure how schema files are searched.

        Args:
            include_package_name: Whether to include package name in search
                patterns
            include_path_to_file: Whether to include intermediate path
                components (e.g., endpoints.catalog)
            path_to_file_separator: How to separate path components in file
                names
            path_to_class_separator: How to separate class/method components
            custom_patterns: Additional custom patterns to try (optional)

        Examples:
            For "perekrestok_api.endpoints.catalog.ProductService.similar":

            SearchPolicy(False, True, PathSeparator.DOT, PathSeparator.DOT):
                → "ProductService.similar.schema.json"
                → "endpoints.catalog.ProductService.similar.schema.json"

            SearchPolicy(False, False, PathSeparator.DOT, PathSeparator.DOT):
                → "ProductService.similar.schema.json" (только класс+метод)

            SearchPolicy(True, True, PathSeparator.SLASH, PathSeparator.DOT):
                → "perekrestok_api/endpoints/catalog/ProductService.similar.schema.json"

            SearchPolicy(False, True, PathSeparator.NONE, PathSeparator.NONE):
                → "ProductServicesimilar.schema.json"
        """
        self.include_package_name = include_package_name
        self.include_path_to_file = include_path_to_file
        self.path_to_file_separator = path_to_file_separator
        self.path_to_class_separator = path_to_class_separator
        self.custom_patterns = custom_patterns or []

    def __repr__(self) -> str:
        return (
            f"SearchPolicy(include_package_name={self.include_package_name}, "
            f"include_path_to_file={self.include_path_to_file}, "
            f"path_to_file_separator={self.path_to_file_separator}, "
            f"path_to_class_separator={self.path_to_class_separator})"
        )
