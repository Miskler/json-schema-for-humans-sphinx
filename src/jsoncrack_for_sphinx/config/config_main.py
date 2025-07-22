"""
Main configuration class.
"""

from typing import List, Optional

from ..search.search_policy import SearchPolicy
from ..utils.types import RenderMode, Theme
from .config_classes import ContainerConfig, RenderConfig


class JsonCrackConfig:
    """Main JSONCrack configuration."""

    def __init__(
        self,
        render: Optional[RenderConfig] = None,
        container: Optional[ContainerConfig] = None,
        theme: Theme = Theme.AUTO,
        search_policy: Optional[SearchPolicy] = None,
        disable_autodoc: bool = False,
        autodoc_ignore: Optional[List[str]] = None,
    ):
        """
        Args:
            render: Render configuration
            container: Container configuration
            theme: Theme setting
            search_policy: Schema file search policy
            disable_autodoc: Disable automatic schema detection in autodoc
            autodoc_ignore: List of full paths to ignore in autodoc
                (uses "not starts with" logic)
        """
        self.render = render or RenderConfig(RenderMode.OnClick())
        self.container = container or ContainerConfig()
        self.theme = theme
        self.search_policy = search_policy or SearchPolicy()
        self.disable_autodoc = disable_autodoc
        self.autodoc_ignore = autodoc_ignore or []

    def __repr__(self) -> str:
        return (
            f"JsonCrackConfig(render={self.render}, "
            f"container={self.container}, theme={self.theme}, "
            f"search_policy={self.search_policy}, "
            f"disable_autodoc={self.disable_autodoc}, "
            f"autodoc_ignore={self.autodoc_ignore})"
        )
