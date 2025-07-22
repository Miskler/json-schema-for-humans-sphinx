"""
Tests for static files (CSS and JavaScript).

This module imports all static file tests from separate modules.
"""

# Import all test classes from separated modules
from .test_file_basics import TestStaticFileContent, TestStaticFileExistence
from .test_functionality import TestStaticFunctionality
from .test_syntax_validation import TestCssSyntax, TestJavaScriptSyntax
from .test_theme_config import TestStaticThemeConfig

# Re-export test classes for pytest discovery
__all__ = [
    "TestStaticFileExistence",
    "TestStaticFileContent",
    "TestCssSyntax",
    "TestJavaScriptSyntax",
    "TestStaticFunctionality",
    "TestStaticThemeConfig",
]
