"""
Main Sphinx extension module for JSONCrack JSON schema visualization.
"""

import json
import logging as std_logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.application import Sphinx
from sphinx.util import logging
from sphinx.util.docutils import SphinxDirective

from .config import JsonCrackConfig, get_config_values, parse_config, SearchPolicy, PathSeparator

logger = logging.getLogger(__name__)


def get_jsoncrack_config(app_config: Any) -> JsonCrackConfig:
    """Get JSONCrack configuration from Sphinx app config."""

    # Try to get new-style config first
    if hasattr(app_config, "jsoncrack_default_options"):
        config_dict = app_config.jsoncrack_default_options
        return parse_config(config_dict)

    # Fall back to old-style config for backward compatibility
    from .config import (
        ContainerConfig,
        Directions,
        JsonCrackConfig,
        RenderConfig,
        RenderMode,
        Theme,
    )

    # Parse render mode
    render_mode_str = getattr(app_config, "jsoncrack_render_mode", "onclick")
    render_mode: Union[RenderMode.OnClick, RenderMode.OnLoad, RenderMode.OnScreen]
    if render_mode_str == "onclick":
        render_mode = RenderMode.OnClick()
    elif render_mode_str == "onload":
        render_mode = RenderMode.OnLoad()
    elif render_mode_str == "onscreen":
        threshold = getattr(app_config, "jsoncrack_onscreen_threshold", 0.1)
        margin = getattr(app_config, "jsoncrack_onscreen_margin", "50px")
        render_mode = RenderMode.OnScreen(threshold=threshold, margin=margin)
    else:
        render_mode = RenderMode.OnClick()

    # Parse direction
    direction_str = getattr(app_config, "jsoncrack_direction", "RIGHT")
    direction = Directions(direction_str)

    # Parse theme
    theme_str = getattr(app_config, "jsoncrack_theme", None)
    if theme_str == "light":
        theme = Theme.LIGHT
    elif theme_str == "dark":
        theme = Theme.DARK
    else:
        theme = Theme.AUTO

    # Parse container settings
    height = getattr(app_config, "jsoncrack_height", "500")
    width = getattr(app_config, "jsoncrack_width", "100%")

    return JsonCrackConfig(
        render=RenderConfig(render_mode),
        container=ContainerConfig(direction=direction, height=height, width=width),
        theme=theme,
    )


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


def find_schema_for_object(
    obj_name: str, schema_dir: str, search_policy: Optional[SearchPolicy] = None
) -> Optional[Tuple[Path, str]]:
    """
    Find schema file for a given object (function/method).

    Args:
        obj_name: Full name of the object (e.g., "example_module.User.create")
        schema_dir: Directory containing schema files
        search_policy: Search policy to use (optional, uses default if None)

    Returns:
        Tuple of (Path to schema file, file type) if found, None otherwise
        File type is either 'schema' for .schema.json files or 'json' for .json files
    """
    logger.debug(f"Looking for schema for object: {obj_name}")
    logger.debug(f"Schema directory: {schema_dir}")
    
    if not schema_dir:
        logger.debug("No schema directory configured")
        return None

    schema_dir_path = Path(schema_dir)
    if not schema_dir_path.exists():
        logger.warning(f"Schema directory does not exist: {schema_dir}")
        return None

    # Use default search policy if none provided
    if search_policy is None:
        search_policy = SearchPolicy()
        logger.debug("Using default search policy")
    else:
        logger.debug(f"Using custom search policy: {search_policy}")

    # Generate search patterns using the policy
    patterns = generate_search_patterns(obj_name, search_policy)

    logger.debug(f"Trying {len(patterns)} patterns:")
    for pattern, file_type in patterns:
        logger.debug(f"  Checking pattern: {pattern}")
        schema_path = schema_dir_path / pattern
        if schema_path.exists():
            logger.info(f"Found schema file: {schema_path} (type: {file_type}) for object: {obj_name}")
            return schema_path, file_type
        else:
            logger.debug(f"    File not found: {schema_path}")

    logger.warning(f"No schema file found for object: {obj_name}")
    return None


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


def autodoc_process_signature(
    app: Sphinx,
    what: str,
    name: str,
    obj: Any,
    options: Dict[str, Any],
    signature: str,
    return_annotation: str,
) -> Optional[Tuple[str, str]]:
    """Process autodoc signatures and add schema information."""
    logger.debug(f"Processing signature for {what}: {name}")
    
    if what not in ("function", "method", "class"):
        logger.debug(f"Skipping {what} (not function/method/class)")
        return None

    config = app.config
    schema_dir = getattr(config, "json_schema_dir", None)

    if not schema_dir:
        logger.debug("No json_schema_dir configured, skipping schema search")
        return None

    logger.debug(f"Searching for schema for {name} in {schema_dir}")

    # Get search policy from configuration
    search_policy = None
    if hasattr(config, "jsoncrack_default_options"):
        jsoncrack_config = get_jsoncrack_config(config)
        search_policy = jsoncrack_config.search_policy
        logger.debug(f"Using search policy from config: {search_policy}")

    # Find schema file
    schema_result = find_schema_for_object(name, schema_dir, search_policy)
    if not schema_result:
        logger.debug(f"No schema found for {name}")
        return None

    schema_path, file_type = schema_result
    logger.info(f"Found schema for {name}: {schema_path} (type: {file_type})")

    # Store schema path and type to be used later
    if not hasattr(app.env, "_jsoncrack_schema_paths"):
        setattr(app.env, "_jsoncrack_schema_paths", {})

    schema_paths = getattr(app.env, "_jsoncrack_schema_paths")
    schema_paths[name] = (str(schema_path), file_type)
    logger.debug(f"Stored schema path for {name}")

    return None


def autodoc_process_docstring(
    app: Sphinx,
    what: str,
    name: str,
    obj: Any,
    options: Dict[str, Any],
    lines: List[str],
) -> None:
    """Process docstrings and add schema HTML."""
    logger.debug(f"Processing docstring for {what}: {name}")
    
    if what not in ("function", "method", "class"):
        logger.debug(f"Skipping {what} (not function/method/class)")
        return

    if not hasattr(app.env, "_jsoncrack_schema_paths"):
        logger.debug("No schema paths stored, skipping")
        return

    schema_paths = getattr(app.env, "_jsoncrack_schema_paths")
    schema_data = schema_paths.get(name)
    if not schema_data:
        logger.debug(f"No schema data found for {name}")
        return

    logger.debug(f"Processing schema for {name}: {schema_data}")

    if isinstance(schema_data, str):
        # Backward compatibility: if it's just a string, assume it's a schema file
        schema_path_str = schema_data
        file_type = "schema"
    else:
        schema_path_str, file_type = schema_data

    schema_path = Path(schema_path_str)
    
    if not schema_path.exists():
        logger.error(f"Schema file does not exist: {schema_path}")
        return

    logger.info(f"Adding schema to docstring for {name}: {schema_path}")

    # Generate schema HTML
    try:
        html_content = generate_schema_html(schema_path, file_type, app.config)
        logger.debug(f"Generated HTML content for {name} (length: {len(html_content)})")
    except Exception as e:
        logger.error(f"Error generating schema HTML for {name}: {e}")
        return

    # Add schema HTML to docstring
    lines.extend(
        [
            "",
            ".. raw:: html",
            "",
            f"   {html_content}",
            "",
        ]
    )
    logger.debug(f"Added schema HTML to docstring for {name}")


def generate_search_patterns(obj_name: str, search_policy: SearchPolicy) -> List[Tuple[str, str]]:
    """
    Generate search patterns based on search policy.
    
    Args:
        obj_name: Full object name (e.g., "perekrestok_api.endpoints.catalog.ProductService.similar")
        search_policy: Search policy configuration
        
    Returns:
        List of (pattern, file_type) tuples to try
    """
    patterns = []
    parts = obj_name.split(".")
    
    # Helper function to join parts with separator
    def join_with_separator(parts_list: List[str], separator: PathSeparator) -> str:
        if separator == PathSeparator.DOT:
            return ".".join(parts_list)
        elif separator == PathSeparator.SLASH:
            return "/".join(parts_list)
        elif separator == PathSeparator.NONE:
            return "".join(parts_list)
        else:
            return ".".join(parts_list)  # fallback
    
    # Add custom patterns first (highest priority)
    for custom_pattern in search_policy.custom_patterns:
        patterns.extend([
            (f"{custom_pattern}.schema.json", "schema"),
            (f"{custom_pattern}.json", "json"),
        ])
    
    if len(parts) >= 2:
        # Strategy 1: Class.method only (most common case)
        if len(parts) >= 2:
            class_method_parts = parts[-2:]  # Last 2 parts: ["ProductService", "similar"]
            class_method = join_with_separator(class_method_parts, search_policy.path_to_class_separator)
            patterns.extend([
                (f"{class_method}.schema.json", "schema"),
                (f"{class_method}.json", "json"),
            ])
        
        # Strategy 2: Path components based on include_path_to_file setting
        if search_policy.include_path_to_file and len(parts) >= 3:
            # Generate intermediate patterns like "catalog.ProductService.similar"
            # Start from the end and work backwards, creating patterns of increasing length
            for i in range(len(parts) - 3, 0, -1):  # Don't include the full path (handled separately)
                partial_parts = parts[i:]
                if len(partial_parts) >= 3:  # At least one path component + class + method
                    partial_path = join_with_separator(partial_parts, search_policy.path_to_file_separator)
                    patterns.extend([
                        (f"{partial_path}.schema.json", "schema"),
                        (f"{partial_path}.json", "json"),
                    ])
            
            # Include intermediate path components like "endpoints.catalog.ProductService.similar"
            if not search_policy.include_package_name and len(parts) >= 3:
                # Remove first part (package): ["endpoints", "catalog", "ProductService", "similar"]
                without_package = parts[1:]
                if search_policy.path_to_file_separator == PathSeparator.SLASH:
                    # Create directory structure: endpoints/catalog/ProductService.similar.schema.json
                    if len(without_package) >= 2:
                        dir_parts = without_package[:-2]  # ["endpoints", "catalog"]
                        class_method_parts = without_package[-2:]  # ["ProductService", "similar"]
                        class_method = join_with_separator(class_method_parts, search_policy.path_to_class_separator)
                        if dir_parts:
                            dir_path = "/".join(dir_parts)
                            patterns.extend([
                                (f"{dir_path}/{class_method}.schema.json", "schema"),
                                (f"{dir_path}/{class_method}.json", "json"),
                            ])
                else:
                    # Use configured separator for path: endpoints.catalog.ProductService.similar
                    full_path = join_with_separator(without_package, search_policy.path_to_file_separator)
                    patterns.extend([
                        (f"{full_path}.schema.json", "schema"),
                        (f"{full_path}.json", "json"),
                    ])
                    
            # Strategy 3: Include package name if requested
            if search_policy.include_package_name:
                if search_policy.path_to_file_separator == PathSeparator.SLASH:
                    # Create full directory structure: perekrestok_api/endpoints/catalog/ProductService.similar.schema.json
                    if len(parts) >= 2:
                        dir_parts = parts[:-2]  # ["perekrestok_api", "endpoints", "catalog"]
                        class_method_parts = parts[-2:]  # ["ProductService", "similar"]
                        class_method = join_with_separator(class_method_parts, search_policy.path_to_class_separator)
                        if dir_parts:
                            dir_path = "/".join(dir_parts)
                            patterns.extend([
                                (f"{dir_path}/{class_method}.schema.json", "schema"),
                                (f"{dir_path}/{class_method}.json", "json"),
                            ])
                else:
                    # Use configured separator for whole path
                    full_path = join_with_separator(parts, search_policy.path_to_file_separator)
                    patterns.extend([
                        (f"{full_path}.schema.json", "schema"),
                        (f"{full_path}.json", "json"),
                    ])
        
        # Strategy 4: Just method name
        method_name = parts[-1]
        patterns.extend([
            (f"{method_name}.schema.json", "schema"),
            (f"{method_name}.json", "json"),
        ])
    
    # Strategy 5: Full object name as is (fallback)
    patterns.extend([
        (f"{obj_name}.schema.json", "schema"),
        (f"{obj_name}.json", "json"),
    ])
    
    # Remove duplicates while preserving order
    seen = set()
    unique_patterns = []
    for pattern, file_type in patterns:
        key = (pattern, file_type)
        if key not in seen:
            seen.add(key)
            unique_patterns.append((pattern, file_type))
    
    return unique_patterns


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
    static_path = Path(__file__).parent / "static"
    app.config.html_static_path.append(str(static_path))
    app.add_css_file("jsoncrack-schema.css")
    app.add_js_file("jsoncrack-sphinx.js")

    logger.info("JSONCrack Sphinx extension initialized")

    return {
        "version": "0.1.0",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
