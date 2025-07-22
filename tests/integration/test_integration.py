"""
Main integration test entry point.

This module imports all integration test suites.
Individual test suites are organized in separate modules:
- test_basic_workflow.py: Basic workflow tests
- test_directive_integration.py: Directive functionality tests
- test_config_integration.py: Configuration and file handling tests
- test_html_integration.py: HTML generation and JSF tests
- test_sphinx_integration.py: Sphinx build tests
"""

# Import all test suites to ensure they are discovered by pytest
from .test_basic_workflow import TestBasicWorkflow
from .test_config_integration import TestConfigIntegration
from .test_directive_integration import TestDirectiveIntegration
from .test_html_integration import TestHtmlGenerationIntegration
from .test_sphinx_integration import TestSphinxIntegration

__all__ = [
    "TestBasicWorkflow",
    "TestDirectiveIntegration",
    "TestConfigIntegration",
    "TestHtmlGenerationIntegration",
    "TestSphinxIntegration",
]
