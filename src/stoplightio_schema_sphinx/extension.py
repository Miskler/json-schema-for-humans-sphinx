"""
Main Sphinx extension module.
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

from json_schema_for_humans import generate
from json_schema_for_humans.generation_configuration import GenerationConfiguration

logger = logging.getLogger(__name__)


class SchemaDirective(SphinxDirective):
    """Directive to manually include a schema in documentation."""
    
    has_content = False
    required_arguments = 1
    optional_arguments = 0
    option_spec = {
        'title': directives.unchanged,
        'description': directives.unchanged,
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
        """Generate HTML from schema file using json-schema-for-humans."""
        # Create configuration for json-schema-for-humans
        config = GenerationConfiguration(
            minify=True,
            deprecated_from_description=True,
            default_from_description=True,
            expand_buttons=True,
            copy_css=False,
            copy_js=False,
            template_name="js",
        )
        
        # Generate HTML directly from schema file
        result = generate.generate_from_schema(
            schema_file=schema_path,
            config=config
        )
        
        return result


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


def generate_schema_html(schema_path: Path) -> str:
    """Generate HTML representation of a JSON schema."""
    try:
        config = GenerationConfiguration(
            minify=True,
            deprecated_from_description=True,
            default_from_description=True,
            expand_buttons=True,
            copy_css=False,
            copy_js=False,
            template_name="js",
        )
        
        result = generate.generate_from_schema(
            schema_file=schema_path,
            config=config
        )
        
        return result
    except Exception as e:
        logger.error(f"Error generating schema HTML for {schema_path}: {e}")
        return ""


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
    
    # Generate HTML
    html_content = generate_schema_html(schema_path)
    if not html_content:
        return None
    
    # Store schema HTML to be added later
    if not hasattr(app.env, 'schema_htmls'):
        app.env.schema_htmls = {}
    
    app.env.schema_htmls[name] = html_content
    
    return None


def autodoc_process_docstring(app: Sphinx, what: str, name: str, obj: Any,
                             options: Dict[str, Any], lines: List[str]) -> None:
    """Process docstrings and add schema HTML."""
    if what not in ('function', 'method', 'class'):
        return
    
    if not hasattr(app.env, 'schema_htmls'):
        return
    
    schema_html = app.env.schema_htmls.get(name)
    if not schema_html:
        return
    
    # Add schema HTML to docstring
    lines.extend([
        '',
        '.. raw:: html',
        '',
        f'   <div class="json-schema-container">',
        f'   {schema_html}',
        f'   </div>',
        '',
    ])


def setup(app: Sphinx) -> Dict[str, Any]:
    """Set up the Sphinx extension."""
    # Add configuration value
    app.add_config_value('json_schema_dir', None, 'env')
    
    # Add directive
    app.add_directive('schema', SchemaDirective)
    
    # Connect to autodoc events
    app.connect('autodoc-process-signature', autodoc_process_signature)
    app.connect('autodoc-process-docstring', autodoc_process_docstring)
    
    # Add CSS for styling
    static_path = Path(__file__).parent / 'static'
    app.config.html_static_path.append(str(static_path))
    app.add_css_file('stoplightio-schema.css')
    
    return {
        'version': '0.1.0',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
