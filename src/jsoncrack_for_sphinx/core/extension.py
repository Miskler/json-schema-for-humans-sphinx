"""
Main Sphinx extension module for JSONCrack JSON schema visualization.
"""

import logging as std_logging
from pathlib import Path
from typing import Any, Dict

from sphinx.application import Sphinx
from sphinx.util import logging

from .autodoc import autodoc_process_docstring, autodoc_process_signature
from .directive import SchemaDirective

logger = logging.getLogger(__name__)


def setup(app: Sphinx) -> Dict[str, Any]:
    """Set up the Sphinx extension."""
    # Add configuration values for new structured config
    app.add_config_value("json_schema_dir", None, "env")
    app.add_config_value("jsoncrack_default_options", {}, "env")
    app.add_config_value("jsoncrack_debug_logging", False, "env")

    # Add configuration values for backward compatibility
    app.add_config_value("jsoncrack_render_mode", "onclick", "env")
    app.add_config_value("jsoncrack_theme", None, "env")
    app.add_config_value("jsoncrack_direction", "RIGHT", "env")
    app.add_config_value("jsoncrack_height", "500", "env")
    app.add_config_value("jsoncrack_width", "100%", "env")
    app.add_config_value("jsoncrack_onscreen_threshold", 0.1, "env")
    app.add_config_value("jsoncrack_onscreen_margin", "50px", "env")
    app.add_config_value("jsoncrack_disable_autodoc", False, "env")
    app.add_config_value("jsoncrack_autodoc_ignore", [], "env")

    # Configure logging level if debug is enabled
    if getattr(app.config, "jsoncrack_debug_logging", False):
        # Enable verbose logging
        std_logger = std_logging.getLogger("jsoncrack_for_sphinx")
        std_logger.setLevel(std_logging.DEBUG)
        logger.info("JSONCrack debug logging enabled")

    # Add directive
    app.add_directive("schema", SchemaDirective)

    # Connect to autodoc events
    app.connect("autodoc-process-signature", autodoc_process_signature)
    app.connect("autodoc-process-docstring", autodoc_process_docstring)

    # Add CSS and JS for styling and functionality
    static_path = Path(__file__).parent.parent / "static"
    app.config.html_static_path.append(str(static_path))
    app.add_css_file("jsoncrack-schema.css")
    app.add_js_file("jsoncrack-sphinx.js")

    logger.info("JSONCrack Sphinx extension initialized")

    return {
        "version": "0.1.0",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
