# Configuration file for the Sphinx documentation builder.

import os
import sys

# Add the example module to the path
sys.path.insert(0, os.path.abspath('..'))

# -- Project information -----------------------------------------------------

project = 'JSON Schema Sphinx Example'
copyright = '2025, Example Author'
author = 'Example Author'
release = '0.1.0'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'jsoncrack_for_sphinx',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------

html_theme = 'alabaster'
html_static_path = ['_static']

# -- Extension configuration -------------------------------------------------

# Configure the schema directory
json_schema_dir = os.path.join(os.path.dirname(__file__), '..', 'schemas')

# JSONCrack configuration
from jsoncrack_for_sphinx.config import RenderMode, Directions, Theme, ContainerConfig, RenderConfig

jsoncrack_default_options = {
    'render': RenderConfig(
        mode=RenderMode.OnScreen(threshold=0.1, margin='50px')
    ),
    'container': ContainerConfig(
        direction=Directions.DOWN,
        height='500',
        width='100%'
    ),
    'theme': Theme.AUTO
}

# Autodoc configuration
autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'show-inheritance': True,
}
