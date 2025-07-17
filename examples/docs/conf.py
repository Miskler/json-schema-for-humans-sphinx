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
jsoncrack_render_mode = 'onclick'  # 'onclick' or 'onload'
jsoncrack_theme = None  # 'light', 'dark' or None (auto-detect from page)
jsoncrack_direction = 'DOWN'  # 'TOP', 'RIGHT', 'DOWN', 'LEFT'
jsoncrack_height = '500'  # в пикселях
jsoncrack_width = '100%'  # в пикселях или процентах

# Autodoc configuration
autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'show-inheritance': True,
}
