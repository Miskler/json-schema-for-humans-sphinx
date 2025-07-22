"""
HTML generation for JSONCrack visualizations.
"""

import json
from pathlib import Path
from typing import Any, Optional

from sphinx.util import logging

from ..config.config_parser import JsonCrackConfig, get_config_values
from ..config.config_utils import get_jsoncrack_config

logger = logging.getLogger(__name__)


def generate_schema_html(
    schema_path: Path, file_type: str, app_config: Optional[Any] = None
) -> str:
    """Generate HTML representation of a JSON schema or JSON data for JSONCrack."""
    logger.debug(f"Generating schema HTML for: {schema_path} (type: {file_type})")

    try:
        # Get configuration
        config = get_jsoncrack_config(app_config) if app_config else JsonCrackConfig()
        config_values = get_config_values(config)
        logger.debug(f"Using config values: {config_values}")

        # Read schema file
        with open(schema_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        logger.debug(f"Successfully loaded JSON data from {schema_path}")

        # Process data based on file type
        if file_type == "schema":
            logger.debug("Processing as JSON schema, attempting to generate fake data")
            # For .schema.json files, generate fake data using JSF
            try:
                from jsf import JSF

                fake_data = JSF(data).generate()
                json_data = fake_data
                logger.debug("Successfully generated fake data using JSF")
            except ImportError:
                logger.warning("jsf library not available, using schema as-is")
                json_data = data
            except Exception as e:
                logger.warning(
                    f"Error generating fake data with JSF: {e}, using schema as-is"
                )
                json_data = data
        else:
            logger.debug("Processing as JSON data file")
            # For .json files, use data as-is
            json_data = data

        # Передаем JSON как строковый атрибут data-schema
        # Используем html.escape для экранирования JSON в HTML-атрибуте
        import html

        schema_str = html.escape(json.dumps(json_data))
        logger.debug(f"Escaped JSON data length: {len(schema_str)}")

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

        logger.info(f"Successfully generated HTML for schema: {schema_path}")
        return html_content
    except Exception as e:
        logger.error(f"Error generating schema HTML for {schema_path}: {e}")
        return f"<div class='error'>Error processing schema file: {str(e)}</div>"
