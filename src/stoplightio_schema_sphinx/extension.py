"""
Main Sphinx extension module for JSONCrack JSON schema visualization.
"""

import os
import json
from typing import Any, Dict, List, Optional, Tuple
from pathlib import Path

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.application import Sphinx
from sphinx.util.docutils import SphinxDirective
from sphinx.ext.autodoc import Documenter
from sphinx.util import logging

logger = logging.getLogger(__name__)


class SchemaDirective(SphinxDirective):
    """Directive to manually include a schema in documentation."""
    
    has_content = False
    required_arguments = 1
    optional_arguments = 0
    option_spec = {
        'title': directives.unchanged,
        'description': directives.unchanged,
        'render_mode': directives.unchanged,
        'theme': directives.unchanged,
        'direction': directives.unchanged,
        'height': directives.unchanged,
        'width': directives.unchanged,
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
            return [nodes.raw('', html_content, format='html')]
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
        
        # Get options from directive or config
        render_mode = self.options.get('render_mode') or getattr(config, 'jsoncrack_render_mode', 'onclick')
        theme = self.options.get('theme') or getattr(config, 'jsoncrack_theme', None)
        direction = self.options.get('direction') or getattr(config, 'jsoncrack_direction', 'RIGHT')
        height = self.options.get('height') or getattr(config, 'jsoncrack_height', '500')
        width = self.options.get('width') or getattr(config, 'jsoncrack_width', '100%')
        
        # Read schema file
        try:
            with open(schema_path, 'r', encoding='utf-8') as f:
                schema_json = json.load(f)
            
            # Передаем JSON как строковый атрибут data-schema
            # Используем html.escape для правильного экранирования JSON в HTML-атрибуте
            import html
            schema_str = html.escape(json.dumps(schema_json))
            
            # Create HTML for JSONCrack visualization
            html_content = f'''
            <div class="jsoncrack-container" 
                 data-schema="{schema_str}"
                 data-render-mode="{render_mode}"
                 data-theme="{theme or ''}"
                 data-direction="{direction}"
                 data-height="{height}"
                 data-width="{width}">
            </div>
            '''
            
            # Add title and description if provided
            if 'title' in self.options or 'description' in self.options:
                title = self.options.get('title', '')
                description = self.options.get('description', '')
                
                if title:
                    html_content = f"<h3>{title}</h3>" + html_content
                if description:
                    html_content = f"<p>{description}</p>" + html_content
            
            return html_content
            
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in schema file {schema_path}: {e}")
            return f"<div class='error'>Error: Invalid JSON in schema file {schema_path.name}</div>"
        except Exception as e:
            logger.error(f"Error processing schema file {schema_path}: {e}")
            return f"<div class='error'>Error processing schema file {schema_path.name}: {str(e)}</div>"


def find_schema_for_object(obj_name: str, schema_dir: str) -> Optional[Path]:
    """
    Find schema file for a given object (function/method).
    
    Args:
        obj_name: Full name of the object (e.g., "MyClass.my_method")
        schema_dir: Directory containing schema files
    
    Returns:
        Path to schema file if found, None otherwise
    """
    if not schema_dir:
        return None
    
    schema_dir_path = Path(schema_dir)
    if not schema_dir_path.exists():
        return None
    
    # Try different naming patterns
    patterns = [
        f"{obj_name}.schema.json",
        f"{obj_name}.json",
    ]
    
    # Also try with option names (for methods with multiple schemas)
    for schema_file in schema_dir_path.glob("*.schema.json"):
        if schema_file.name.startswith(f"{obj_name}."):
            patterns.append(schema_file.name)
    
    for pattern in patterns:
        schema_path = schema_dir_path / pattern
        if schema_path.exists():
            return schema_path
    
    return None


def generate_schema_html(schema_path: Path, app_config=None) -> str:
    """Generate HTML representation of a JSON schema for JSONCrack."""
    try:
        # Default config values if not provided
        render_mode = getattr(app_config, 'jsoncrack_render_mode', 'onclick') if app_config else 'onclick'
        theme = getattr(app_config, 'jsoncrack_theme', None) if app_config else None
        direction = getattr(app_config, 'jsoncrack_direction', 'RIGHT') if app_config else 'RIGHT'
        height = getattr(app_config, 'jsoncrack_height', '500') if app_config else '500'
        width = getattr(app_config, 'jsoncrack_width', '100%') if app_config else '100%'
        
        # Read schema file
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema_json = json.load(f)
            
        # Передаем JSON как строковый атрибут data-schema
        # Используем html.escape для экранирования JSON в HTML-атрибуте
        import html
        schema_str = html.escape(json.dumps(schema_json))
        
        # Create HTML for JSONCrack visualization
        html_content = f'''
        <div class="jsoncrack-container" 
             data-schema="{schema_str}" 
             data-render-mode="{render_mode}"
             data-theme="{theme or ''}"
             data-direction="{direction}"
             data-height="{height}"
             data-width="{width}">
        </div>
        '''
        
        return html_content
    except Exception as e:
        logger.error(f"Error generating schema HTML for {schema_path}: {e}")
        return f"<div class='error'>Error processing schema file: {str(e)}</div>"


def autodoc_process_signature(app: Sphinx, what: str, name: str, obj: Any, 
                             options: Dict[str, Any], signature: str, 
                             return_annotation: str) -> Optional[Tuple[str, str]]:
    """Process autodoc signatures and add schema information."""
    if what not in ('function', 'method', 'class'):
        return None
    
    config = app.config
    schema_dir = getattr(config, 'json_schema_dir', None)
    
    if not schema_dir:
        return None
    
    # Find schema file
    schema_path = find_schema_for_object(name, schema_dir)
    if not schema_path:
        return None
    
    # Store schema path to be used later
    if not hasattr(app.env, '_jsoncrack_schema_paths'):
        setattr(app.env, '_jsoncrack_schema_paths', {})
    
    schema_paths = getattr(app.env, '_jsoncrack_schema_paths')
    schema_paths[name] = str(schema_path)
    
    return None


def autodoc_process_docstring(app: Sphinx, what: str, name: str, obj: Any,
                             options: Dict[str, Any], lines: List[str]) -> None:
    """Process docstrings and add schema HTML."""
    if what not in ('function', 'method', 'class'):
        return
    
    if not hasattr(app.env, '_jsoncrack_schema_paths'):
        return
    
    schema_paths = getattr(app.env, '_jsoncrack_schema_paths')
    schema_path_str = schema_paths.get(name)
    if not schema_path_str:
        return
    
    schema_path = Path(schema_path_str)
    
    # Generate schema HTML
    html_content = generate_schema_html(schema_path, app.config)
    
    # Add schema HTML to docstring
    lines.extend([
        '',
        '.. raw:: html',
        '',
        f'   {html_content}',
        '',
    ])


def setup(app: Sphinx) -> Dict[str, Any]:
    """Set up the Sphinx extension."""
    # Add configuration values
    app.add_config_value('json_schema_dir', None, 'env')
    app.add_config_value('jsoncrack_render_mode', 'onclick', 'env')
    app.add_config_value('jsoncrack_theme', None, 'env')
    app.add_config_value('jsoncrack_direction', 'RIGHT', 'env')
    app.add_config_value('jsoncrack_height', '500', 'env')
    app.add_config_value('jsoncrack_width', '100%', 'env')
    
    # Add directive
    app.add_directive('schema', SchemaDirective)
    
    # Connect to autodoc events
    app.connect('autodoc-process-signature', autodoc_process_signature)
    app.connect('autodoc-process-docstring', autodoc_process_docstring)
    
    # Add CSS and JS for styling and functionality
    static_path = Path(__file__).parent / 'static'
    app.config.html_static_path.append(str(static_path))
    app.add_css_file('jsoncrack-schema.css')
    app.add_js_file('jsoncrack-sphinx.js')
    
    return {
        'version': '0.1.0',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
