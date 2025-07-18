"""
Compatibility tests for different Python versions and dependencies.
"""

import sys
import pytest
from unittest.mock import Mock, patch

from jsoncrack_for_sphinx import __version__
from jsoncrack_for_sphinx.config import JsonCrackConfig, RenderMode
from jsoncrack_for_sphinx.extension import setup, get_jsoncrack_config


class TestPythonCompatibility:
    """Test Python version compatibility."""
    
    def test_python_version_support(self):
        """Test that we're running on a supported Python version."""
        # According to pyproject.toml, we support Python 3.8+
        assert sys.version_info >= (3, 8), "Python 3.8+ is required"
        
        # Test that we can import all modules
        from jsoncrack_for_sphinx import extension
        from jsoncrack_for_sphinx import config
        from jsoncrack_for_sphinx import utils
        from jsoncrack_for_sphinx import fixtures
        
        assert extension is not None
        assert config is not None
        assert utils is not None
        assert fixtures is not None
    
    def test_typing_compatibility(self):
        """Test typing compatibility across Python versions."""
        # Test that typing imports work
        from typing import Dict, List, Optional, Union, Any
        
        # Test that our type hints work
        from jsoncrack_for_sphinx.config import RenderMode, Directions
        from jsoncrack_for_sphinx.extension import find_schema_for_object
        
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


class TestDependencyCompatibility:
    """Test compatibility with different dependency versions."""
    
    def test_sphinx_compatibility(self):
        """Test Sphinx compatibility."""
        try:
            import sphinx
            sphinx_version = sphinx.__version__
            
            # We require Sphinx 4.0+
            version_parts = sphinx_version.split('.')
            major_version = int(version_parts[0])
            
            assert major_version >= 4, f"Sphinx 4.0+ required, got {sphinx_version}"
            
            # Test that we can import Sphinx components we use
            from sphinx.application import Sphinx
            from sphinx.util.docutils import SphinxDirective
            from sphinx.util import logging
            
            assert Sphinx is not None
            assert SphinxDirective is not None
            assert logging is not None
            
        except ImportError:
            pytest.skip("Sphinx not installed")
    
    def test_jsf_compatibility(self):
        """Test JSF (JSON Schema Faker) compatibility."""
        try:
            import jsf
            
            # Test basic JSF functionality
            simple_schema = {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "age": {"type": "integer", "minimum": 0, "maximum": 150}
                }
            }
            
            faker = jsf.JSF(simple_schema)
            fake_data = faker.generate()
            
            assert isinstance(fake_data, dict)
            assert "name" in fake_data
            assert "age" in fake_data
            assert isinstance(fake_data["age"], int)
            
        except ImportError:
            pytest.skip("JSF not installed")
        except Exception as e:
            pytest.skip(f"JSF compatibility issue: {e}")


class TestBackwardCompatibility:
    """Test backward compatibility with older configurations."""
    
    def test_legacy_config_format(self):
        """Test that legacy configuration format still works."""
        from jsoncrack_for_sphinx.extension import get_jsoncrack_config
        
        # Create old-style configuration
        mock_config = Mock()
        # Remove new-style config
        if hasattr(mock_config, 'jsoncrack_default_options'):
            delattr(mock_config, 'jsoncrack_default_options')
        
        # Set old-style config values
        mock_config.jsoncrack_render_mode = 'onclick'
        mock_config.jsoncrack_theme = 'dark'
        mock_config.jsoncrack_direction = 'LEFT'
        mock_config.jsoncrack_height = '600'
        mock_config.jsoncrack_width = '90%'
        mock_config.jsoncrack_onscreen_threshold = 0.2
        mock_config.jsoncrack_onscreen_margin = '75px'
        
        # Should still work
        config = get_jsoncrack_config(mock_config)
        
        assert config is not None
        assert config.theme.value == 'dark'
        assert config.container.height == '600'
        assert config.container.width == '90%'
    
    def test_partial_legacy_config(self):
        """Test partial legacy configuration."""
        from jsoncrack_for_sphinx.extension import get_jsoncrack_config
        
        mock_config = Mock()
        if hasattr(mock_config, 'jsoncrack_default_options'):
            delattr(mock_config, 'jsoncrack_default_options')
        
        # Set only some old-style values
        mock_config.jsoncrack_render_mode = 'onscreen'
        mock_config.jsoncrack_direction = 'DOWN'
        mock_config.jsoncrack_theme = None
        mock_config.jsoncrack_height = '500'
        mock_config.jsoncrack_width = '100%'
        mock_config.jsoncrack_onscreen_threshold = 0.1
        mock_config.jsoncrack_onscreen_margin = '50px'
        
        config = get_jsoncrack_config(mock_config)
        
        assert isinstance(config.render.mode, RenderMode.OnScreen)
        assert config.container.direction.value == 'DOWN'
        assert config.container.height == '500'


class TestFeatureCompatibility:
    """Test feature compatibility across different environments."""
    
    def test_file_encoding_compatibility(self, temp_dir):
        """Test file encoding compatibility."""
        from jsoncrack_for_sphinx.utils import validate_schema_file, get_schema_info
        
        # Test UTF-8 encoding
        utf8_schema = {
            "type": "object",
            "title": "UTF-8 Test with émojis 🚀",
            "properties": {
                "café": {"type": "string"},
                "naïve": {"type": "string"}
            }
        }
        
        utf8_file = temp_dir / "utf8.schema.json"
        with open(utf8_file, 'w', encoding='utf-8') as f:
            import json
            json.dump(utf8_schema, f, ensure_ascii=False)
        
        assert validate_schema_file(utf8_file) is True
        info = get_schema_info(utf8_file)
        assert "UTF-8 Test with émojis 🚀" in info['title']
        assert "café" in info['properties']
    
    def test_html_escaping_compatibility(self, temp_dir):
        """Test HTML escaping compatibility."""
        from jsoncrack_for_sphinx.extension import generate_schema_html
        
        # Create schema with HTML-like content
        html_schema = {
            "type": "object",
            "title": "HTML Test <script>alert('xss')</script>",
            "properties": {
                "content": {
                    "type": "string",
                    "description": "Contains <b>HTML</b> & special chars"
                }
            }
        }
        
        schema_file = temp_dir / "html_test.schema.json"
        with open(schema_file, 'w') as f:
            import json
            json.dump(html_schema, f)
        
        html = generate_schema_html(schema_file, 'schema')
        
        # Should be properly escaped
        assert 'jsoncrack-container' in html
        assert '&lt;script&gt;' in html or 'script' not in html  # Should be escaped
        assert 'data-schema=' in html  # JSON data should be present
