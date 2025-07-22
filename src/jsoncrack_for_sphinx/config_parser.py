"""
Configuration parsing utilities.
"""

from typing import Any, Dict, Optional

from .config_classes import ContainerConfig, RenderConfig
from .search_policy import SearchPolicy
from .types import Directions, PathSeparator, RenderMode, Theme


class JsonCrackConfig:
    """Main JSONCrack configuration."""

    def __init__(
        self,
        render: Optional[RenderConfig] = None,
        container: Optional[ContainerConfig] = None,
        theme: Theme = Theme.AUTO,
        search_policy: Optional[SearchPolicy] = None,
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
                custom_patterns=custom_patterns,
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
