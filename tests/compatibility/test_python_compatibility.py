"""
Python version compatibility tests.
"""

import sys


class TestPythonCompatibility:
    """Test Python version compatibility."""

    def test_python_version_support(self):
        """Test that we're running on a supported Python version."""
        # According to pyproject.toml, we support Python 3.8+
        assert sys.version_info >= (3, 8), "Python 3.8+ is required"

        # Test that we can import all modules
        from jsoncrack_for_sphinx import config, extension, fixtures, utils

        assert extension is not None
        assert config is not None
        assert utils is not None
        assert fixtures is not None

    def test_typing_compatibility(self):
        """Test typing compatibility across Python versions."""
        # Test that typing imports work
        from typing import Any, Dict, List, Optional, Union

        # Test that our type hints work
        # These should not raise type errors
        assert Dict is not None
        assert List is not None
        assert Optional is not None
        assert Union is not None
        assert Any is not None

    def test_json_compatibility(self):
        """Test JSON handling compatibility."""
        import json

        # Test basic JSON operations
        test_data = {"type": "object", "properties": {"name": {"type": "string"}}}
        json_str = json.dumps(test_data)
        parsed_data = json.loads(json_str)

        assert parsed_data == test_data
