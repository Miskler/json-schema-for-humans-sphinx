"""
Configuration parsing functions.
"""

from typing import Any, Dict

from ..search.search_policy import SearchPolicy
from ..utils.types import Directions, PathSeparator, RenderMode, Theme
from .config_classes import ContainerConfig, RenderConfig
from .config_main import JsonCrackConfig


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
            if isinstance(mode_obj, str):
                # Convert string to RenderMode object
                if mode_obj == "onclick":
                    mode_obj = RenderMode.OnClick()
                elif mode_obj == "onload":
                    mode_obj = RenderMode.OnLoad()
                elif mode_obj == "onscreen":
                    threshold = render_obj.get("threshold", 0.1)
                    margin = render_obj.get("margin", "50px")
                    mode_obj = RenderMode.OnScreen(threshold=threshold, margin=margin)
                else:
                    # Default to onclick for unknown modes
                    mode_obj = RenderMode.OnClick()
            elif isinstance(mode_obj, dict) and "type" in mode_obj:
                # Handle nested mode object
                mode_type = mode_obj["type"]
                if mode_type == "onclick":
                    mode_obj = RenderMode.OnClick()
                elif mode_type == "onload":
                    mode_obj = RenderMode.OnLoad()
                elif mode_type == "onscreen":
                    threshold = mode_obj.get("threshold", 0.1)
                    margin = mode_obj.get("margin", "50px")
                    mode_obj = RenderMode.OnScreen(threshold=threshold, margin=margin)
                else:
                    # Default to onclick for unknown modes
                    mode_obj = RenderMode.OnClick()
            else:
                # Fallback for any other type
                mode_obj = RenderMode.OnClick()
            render_config = RenderConfig(mode_obj)

    # Parse container config
    container_config = None
    if "container" in config_dict:
        container_obj = config_dict["container"]
        if isinstance(container_obj, ContainerConfig):
            container_config = container_obj
        elif isinstance(container_obj, dict):
            # Legacy format support
            direction_str = container_obj.get("direction", "RIGHT")
            if isinstance(direction_str, str):
                if direction_str == "LEFT":
                    direction = Directions.LEFT
                elif direction_str == "RIGHT":
                    direction = Directions.RIGHT
                elif direction_str == "TOP":
                    direction = Directions.TOP
                elif direction_str == "DOWN":
                    direction = Directions.DOWN
                else:
                    # Default to RIGHT for unknown directions
                    direction = Directions.RIGHT
            else:
                direction = direction_str

            container_config = ContainerConfig(
                direction=direction,
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
    theme_obj = config_dict.get("theme", Theme.AUTO)
    if isinstance(theme_obj, str):
        if theme_obj == "light":
            theme = Theme.LIGHT
        elif theme_obj == "dark":
            theme = Theme.DARK
        elif theme_obj == "auto":
            theme = Theme.AUTO
        else:
            theme = Theme.AUTO
    else:
        theme = theme_obj

    return JsonCrackConfig(
        render=render_config or RenderConfig(RenderMode.OnClick()),
        container=container_config or ContainerConfig(),
        theme=theme,
        search_policy=search_policy or SearchPolicy(),
        disable_autodoc=config_dict.get("disable_autodoc", False),
        autodoc_ignore=config_dict.get("autodoc_ignore", []),
    )
