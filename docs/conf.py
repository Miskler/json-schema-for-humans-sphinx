"""
Configuration file for the Sphinx documentation builder.
"""

import os
import sys

# Add the source directory to the path
sys.path.insert(0, os.path.abspath('../src'))
# Add the examples directory to the path
sys.path.insert(0, os.path.abspath('../examples'))

# -- Project information -----------------------------------------------------

project = 'JSONCrack Sphinx Extension'
copyright = '2025, Miskler'
author = 'Miskler'
release = '0.1.0'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'jsoncrack_for_sphinx',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------

html_theme = 'furo'
html_static_path = ['_static']

# Custom CSS files
html_css_files = [
    'custom.css',
]

# -- Furo theme options -------------------------------------------------

html_theme_options = {
    "sidebar_hide_name": True,
    "navigation_with_keys": True,
    "top_of_page_button": "edit",
    "source_repository": "https://github.com/miskler/jsoncrack-for-sphinx",
    "source_branch": "main",
    "source_directory": "docs/",
    "light_css_variables": {
        "color-brand-primary": "#2563eb",
        "color-brand-content": "#2563eb",
        "color-brand-secondary": "#1d4ed8",
        "color-admonition-title--note": "#2563eb",
        "color-admonition-title-background--note": "#eff6ff",
    },
    "dark_css_variables": {
        "color-brand-primary": "#60a5fa",
        "color-brand-content": "#60a5fa",
        "color-brand-secondary": "#3b82f6",
        "color-admonition-title--note": "#60a5fa",
        "color-admonition-title-background--note": "#1e3a8a",
    }
}

# Configure the schema directory for examples
json_schema_dir = os.path.join(os.path.dirname(__file__), '..', 'examples', 'schemas')

# JSONCrack configuration
from jsoncrack_for_sphinx.config import RenderMode, Directions, Theme, ContainerConfig, RenderConfig, SearchPolicy, PathSeparator

jsoncrack_default_options = {
    'render': RenderConfig(
        mode=RenderMode.OnScreen(threshold=0.1, margin='50px')
    ),
    'container': ContainerConfig(
        direction=Directions.DOWN,
        height='500',
        width='100%'
    ),
    'theme': Theme.AUTO,
    'search_policy': SearchPolicy(
        include_package_name=False,
        path_to_file_separator=PathSeparator.DOT,
        path_to_class_separator=PathSeparator.DOT,
        custom_patterns=[]
    )
}

# Enable debug logging for JSONCrack extension
jsoncrack_debug_logging = True

# -- Extension configuration -------------------------------------------------

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True

# Intersphinx mapping
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}

# Autodoc settings
autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'show-inheritance': True,
}

# Todo settings
todo_include_todos = True
