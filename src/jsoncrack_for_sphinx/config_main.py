"""
Main configuration class.
"""

from typing import Optional

from .config_classes import ContainerConfig, RenderConfig
from .search_policy import SearchPolicy
from .types import RenderMode, Theme


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
