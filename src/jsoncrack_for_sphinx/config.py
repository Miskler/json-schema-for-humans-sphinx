"""
Configuration classes for JSONCrack Sphinx extension.
"""

from enum import Enum
from typing import Any, Dict, Union, Optional


class RenderMode:
    """Render mode configuration classes."""

    class OnClick:
        """Click to load mode - loads when user clicks the button."""

        def __init__(self) -> None:
            self.mode = "onclick"

        def __repr__(self) -> str:
            return "RenderMode.OnClick()"

    class OnLoad:
        """Immediate load mode - loads when page loads."""

        def __init__(self) -> None:
            self.mode = "onload"

        def __repr__(self) -> str:
            return "RenderMode.OnLoad()"

    class OnScreen:
        """Viewport load mode - loads when element becomes visible."""

        def __init__(self, threshold: float = 0.1, margin: str = "50px") -> None:
            """
            Args:
                threshold: Visibility threshold (0.0-1.0)
                margin: Root margin for early loading (e.g., '50px')
            """
            self.mode = "onscreen"
            self.threshold = threshold
            self.margin = margin

        def __repr__(self) -> str:
            return (
                f"RenderMode.OnScreen(threshold={self.threshold}, "
                f"margin='{self.margin}')"
            )


class Directions(Enum):
    """JSONCrack visualization directions."""

    TOP = "TOP"
    RIGHT = "RIGHT"
    DOWN = "DOWN"
    LEFT = "LEFT"


class Theme(Enum):
    """Theme options."""

    LIGHT = "light"
    DARK = "dark"
    AUTO = None  # Auto-detect from page


class PathSeparator(Enum):
    """Path separator options for schema file search."""
    
    DOT = "."          # Use dots: Class.method.schema.json
    SLASH = "/"        # Use slashes: Class/method.schema.json  
    NONE = "none"      # No separator: Classmethod.schema.json


class ContainerConfig:
    """Container configuration."""

    def __init__(
        self,
        direction: Directions = Directions.RIGHT,
        height: Union[int, str] = "500",
        width: Union[int, str] = "100%",
    ):
        """
        Args:
            direction: Visualization direction
            height: Container height in pixels or string
            width: Container width in pixels, percentage, or string
        """
        self.direction = direction
        self.height = str(height)
        self.width = str(width)

    def __repr__(self) -> str:
        return (
            f"ContainerConfig(direction={self.direction}, "
            f"height='{self.height}', width='{self.width}')"
        )


class RenderConfig:
    """Render configuration."""

    def __init__(
        self, mode: Union[RenderMode.OnClick, RenderMode.OnLoad, RenderMode.OnScreen]
    ):
        """
        Args:
            mode: Render mode instance
        """
        self.mode = mode

    def __repr__(self) -> str:
        return f"RenderConfig(mode={self.mode})"


class SearchPolicy:
    """Schema file search policy configuration."""
    
    def __init__(
        self,
        include_package_name: bool = False,
        include_path_to_file: bool = True,
        path_to_file_separator: PathSeparator = PathSeparator.DOT,
        path_to_class_separator: PathSeparator = PathSeparator.DOT,
        custom_patterns: Optional[list] = None
    ):
        """
        Configure how schema files are searched.
        
        Args:
            include_package_name: Whether to include package name in search patterns
            include_path_to_file: Whether to include intermediate path components (e.g., endpoints.catalog)
            path_to_file_separator: How to separate path components in file names
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


class JsonCrackConfig:
    """Main JSONCrack configuration."""

    def __init__(
        self,
        render: Union[RenderConfig, None] = None,
        container: Union[ContainerConfig, None] = None,
        theme: Theme = Theme.AUTO,
        search_policy: Union[SearchPolicy, None] = None,
    ):
        """
        Args:
            render: Render configuration
            container: Container configuration
            theme: Theme setting
            search_policy: Schema file search policy
        """
        self.render = render or RenderConfig(RenderMode.OnClick())
        self.container = container or ContainerConfig()
        self.theme = theme
        self.search_policy = search_policy or SearchPolicy()

    def __repr__(self) -> str:
        return (
            f"JsonCrackConfig(render={self.render}, "
            f"container={self.container}, theme={self.theme}, "
            f"search_policy={self.search_policy})"
        )


def parse_config(config_dict: Dict[str, Any]) -> JsonCrackConfig:
    """Parse configuration dictionary into JsonCrackConfig object."""

    # Handle Mock objects in tests
    if not isinstance(config_dict, dict):
        return JsonCrackConfig()

    # Parse render config
    render_config = None
    if "render" in config_dict:
        render_obj = config_dict["render"]
        if isinstance(render_obj, RenderConfig):
            render_config = render_obj
        elif isinstance(render_obj, dict) and "mode" in render_obj:
            # Legacy format support
            mode_obj = render_obj["mode"]
            render_config = RenderConfig(mode_obj)

    # Parse container config
    container_config = None
    if "container" in config_dict:
        container_obj = config_dict["container"]
        if isinstance(container_obj, ContainerConfig):
            container_config = container_obj
        elif isinstance(container_obj, dict):
            # Legacy format support
            container_config = ContainerConfig(
                direction=container_obj.get("direction", Directions.RIGHT),
                height=container_obj.get("height", "500"),
                width=container_obj.get("width", "100%"),
            )

    # Parse search policy
    search_policy = None
    if "search_policy" in config_dict:
        policy_obj = config_dict["search_policy"]
        if isinstance(policy_obj, SearchPolicy):
            search_policy = policy_obj
        elif isinstance(policy_obj, dict):
            # Parse from dictionary
            include_package = policy_obj.get("include_package_name", False)
            include_path = policy_obj.get("include_path_to_file", True)
            
            # Parse path separators
            path_to_file = policy_obj.get("path_to_file_separator", ".")
            if isinstance(path_to_file, str):
                if path_to_file == ".":
                    path_to_file = PathSeparator.DOT
                elif path_to_file == "/":
                    path_to_file = PathSeparator.SLASH
                elif path_to_file.lower() == "none":
                    path_to_file = PathSeparator.NONE
                else:
                    path_to_file = PathSeparator.DOT
                    
            path_to_class = policy_obj.get("path_to_class_separator", ".")
            if isinstance(path_to_class, str):
                if path_to_class == ".":
                    path_to_class = PathSeparator.DOT
                elif path_to_class == "/":
                    path_to_class = PathSeparator.SLASH
                elif path_to_class.lower() == "none":
                    path_to_class = PathSeparator.NONE
                else:
                    path_to_class = PathSeparator.DOT
                    
            custom_patterns = policy_obj.get("custom_patterns", [])
            
            search_policy = SearchPolicy(
                include_package_name=include_package,
                include_path_to_file=include_path,
                path_to_file_separator=path_to_file,
                path_to_class_separator=path_to_class,
                custom_patterns=custom_patterns
            )

    # Parse theme
    theme = config_dict.get("theme", Theme.AUTO)

    return JsonCrackConfig(
        render=render_config or RenderConfig(RenderMode.OnClick()),
        container=container_config or ContainerConfig(),
        theme=theme,
        search_policy=search_policy or SearchPolicy(),
    )


def get_config_values(config: JsonCrackConfig) -> Dict[str, Any]:
    """Extract configuration values for HTML generation."""

    # Get render mode settings
    render_mode = config.render.mode.mode
    onscreen_threshold = 0.1
    onscreen_margin = "50px"

    # Only get threshold and margin for OnScreen mode
    if isinstance(config.render.mode, RenderMode.OnScreen):
        onscreen_threshold = config.render.mode.threshold
        onscreen_margin = config.render.mode.margin

    # Get theme value
    theme_value = config.theme.value if config.theme != Theme.AUTO else None

    return {
        "render_mode": render_mode,
        "theme": theme_value,
        "direction": config.container.direction.value,
        "height": config.container.height,
        "width": config.container.width,
        "onscreen_threshold": onscreen_threshold,
        "onscreen_margin": onscreen_margin,
    }
