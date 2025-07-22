"""
Sphinx directive for manual schema inclusion.
"""

import json
from pathlib import Path
from typing import List, Optional

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.util import logging
from sphinx.util.docutils import SphinxDirective

from ..config import get_config_values
from ..config.config_utils import get_jsoncrack_config

logger = logging.getLogger(__name__)


class SchemaDirective(SphinxDirective):
    """Directive to manually include a schema in documentation."""

    has_content = False
    required_arguments = 1
    optional_arguments = 0
    option_spec = {
        "title": directives.unchanged,
        "description": directives.unchanged,
        "render_mode": directives.unchanged,
        "theme": directives.unchanged,
        "direction": directives.unchanged,
        "height": directives.unchanged,
        "width": directives.unchanged,
        "onscreen_threshold": directives.unchanged,
        "onscreen_margin": directives.unchanged,
    }

    def run(self) -> List[nodes.Node]:
        """Process the schema directive."""
        schema_name = self.arguments[0]
        config = self.env.config

        schema_path = self._find_schema_file(schema_name, config.json_schema_dir)
        if not schema_path:
            logger.warning(f"Schema file not found: {schema_name}")
            return []

        try:
            html_content = self._generate_schema_html(schema_path)
            return [nodes.raw("", html_content, format="html")]
        except Exception as e:
            logger.error(f"Error generating schema HTML: {e}")
            return []

    def _find_schema_file(self, schema_name: str, schema_dir: str) -> Optional[Path]:
        """Find schema file by name."""
        if not schema_dir:
            return None

        schema_dir_path = Path(schema_dir)
        if not schema_dir_path.exists():
            return None

        # Try different file patterns
        patterns = [
            f"{schema_name}.schema.json",
            f"{schema_name}.json",
        ]

        for pattern in patterns:
            schema_path = schema_dir_path / pattern
            if schema_path.exists():
                return schema_path

        return None

    def _generate_schema_html(self, schema_path: Path) -> str:
        """Generate HTML for JSONCrack visualization of a schema file."""
        config = self.env.config

        # Get configuration
        jsoncrack_config = get_jsoncrack_config(config)
        config_values = get_config_values(jsoncrack_config)

        # Override with directive options if provided
        if "render_mode" in self.options:
            config_values["render_mode"] = self.options["render_mode"]
        if "theme" in self.options:
            config_values["theme"] = self.options["theme"]
        if "direction" in self.options:
            config_values["direction"] = self.options["direction"]
        if "height" in self.options:
            config_values["height"] = self.options["height"]
        if "width" in self.options:
            config_values["width"] = self.options["width"]
        if "onscreen_threshold" in self.options:
            config_values["onscreen_threshold"] = self.options["onscreen_threshold"]
        if "onscreen_margin" in self.options:
            config_values["onscreen_margin"] = self.options["onscreen_margin"]

        # Read schema file
        try:
            with open(schema_path, "r", encoding="utf-8") as f:
                schema_json = json.load(f)

            # Передаем JSON как строковый атрибут data-schema
            # Используем html.escape для правильного экранирования JSON в HTML-атрибуте
            import html

            schema_str = html.escape(json.dumps(schema_json))

            # Create HTML for JSONCrack visualization
            html_content = f"""
            <div class="jsoncrack-container"
                 data-schema="{schema_str}"
                 data-render-mode="{config_values['render_mode']}"
                 data-theme="{config_values['theme'] or ''}"
                 data-direction="{config_values['direction']}"
                 data-height="{config_values['height']}"
                 data-width="{config_values['width']}"
                 data-onscreen-threshold="{config_values['onscreen_threshold']}"
                 data-onscreen-margin="{config_values['onscreen_margin']}">
            </div>
            """

            # Add title and description if provided
            if "title" in self.options or "description" in self.options:
                title = self.options.get("title", "")
                description = self.options.get("description", "")

                if title:
                    html_content = f"<h3>{title}</h3>" + html_content
                if description:
                    html_content = f"<p>{description}</p>" + html_content

            return html_content

        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in schema file {schema_path}: {e}")
            return (
                f"<div class='error'>Error: Invalid JSON in "
                f"schema file {schema_path.name}</div>"
            )
        except Exception as e:
            logger.error(f"Error processing schema file {schema_path}: {e}")
            return (
                f"<div class='error'>Error processing schema file "
                f"{schema_path.name}: {str(e)}</div>"
            )
