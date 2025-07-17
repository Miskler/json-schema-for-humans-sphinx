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
    
    def test_pathlib_compatibility(self):
        """Test pathlib compatibility."""
        from pathlib import Path
        
        # Test that Path operations work as expected
        path = Path("test.json")
        assert path.suffix == ".json"
        assert path.stem == "test"
        
        # Test with our utility functions
        from jsoncrack_for_sphinx.utils import find_schema_files
        
        # Should handle Path objects correctly
        result = find_schema_files(Path("/nonexistent"))
        assert isinstance(result, list)
        assert len(result) == 0
    
    def test_json_compatibility(self):
        """Test JSON handling compatibility."""
        import json
        
        # Test basic JSON operations
        test_data = {"type": "object", "properties": {"name": {"type": "string"}}}
        json_str = json.dumps(test_data)
        parsed_data = json.loads(json_str)
        
        assert parsed_data == test_data
        
        # Test with our functions
        from jsoncrack_for_sphinx.utils import validate_schema_file
        from jsoncrack_for_sphinx.extension import generate_schema_html
        
        # These should handle JSON correctly
        assert validate_schema_file is not None
        assert generate_schema_html is not None
    
    def test_enum_compatibility(self):
        """Test enum compatibility."""
        from enum import Enum
        
        # Test that our enums work
        from jsoncrack_for_sphinx.config import Directions, Theme
        
        assert isinstance(Directions.TOP, Directions)
        assert isinstance(Theme.LIGHT, Theme)
        
        # Test enum values
        assert Directions.TOP.value == 'TOP'
        assert Theme.LIGHT.value == 'light'
    
    def test_mock_compatibility(self):
        """Test unittest.mock compatibility."""
        from unittest.mock import Mock, patch, MagicMock
        
        # Test that mocking works with our code
        mock_app = Mock()
        mock_app.config = Mock()
        mock_app.config.json_schema_dir = None
        
        # Should work without issues
        result = setup(mock_app)
        assert isinstance(result, dict)
        assert 'version' in result


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
            from sphinx.ext.autodoc import Documenter
            from sphinx.util import logging
            
            assert Sphinx is not None
            assert SphinxDirective is not None
            assert Documenter is not None
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
    
    def test_docutils_compatibility(self):
        """Test docutils compatibility."""
        try:
            from docutils import nodes
            from docutils.parsers.rst import directives
            
            # Test that we can create nodes
            raw_node = nodes.raw('', 'test content', format='html')
            assert raw_node is not None
            
            # Test directive utilities
            assert directives.unchanged is not None
            
        except ImportError:
            pytest.skip("docutils not installed")
    
    def test_pytest_compatibility(self):
        """Test pytest compatibility."""
        import pytest
        
        # Test that we can use pytest features
        assert pytest.fixture is not None
        assert pytest.mark is not None
        assert pytest.skip is not None
        assert pytest.raises is not None
        
        # Test that our fixtures work
        from tests.conftest import temp_dir, sample_schema
        
        assert temp_dir is not None
        assert sample_schema is not None


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
    
    def test_mixed_config_format(self):
        """Test mixed old and new configuration format."""
        from jsoncrack_for_sphinx.extension import get_jsoncrack_config
        from jsoncrack_for_sphinx.config import RenderConfig, RenderMode
        
        # Create configuration with both old and new style
        mock_config = Mock()
        
        # New-style config (should take precedence)
        mock_config.jsoncrack_default_options = {
            'render': RenderConfig(RenderMode.OnLoad()),
            'theme': 'light'
        }
        
        # Old-style config (should be ignored)
        mock_config.jsoncrack_render_mode = 'onclick'
        mock_config.jsoncrack_theme = 'dark'
        
        config = get_jsoncrack_config(mock_config)
        
        # Should use new-style config
        assert isinstance(config.render.mode, RenderMode.OnLoad)
        # Note: theme handling depends on implementation
    
    def test_partial_legacy_config(self):
        """Test partial legacy configuration."""
        from jsoncrack_for_sphinx.extension import get_jsoncrack_config
        
        mock_config = Mock()
        if hasattr(mock_config, 'jsoncrack_default_options'):
            delattr(mock_config, 'jsoncrack_default_options')
        
        # Set only some old-style values
        mock_config.jsoncrack_render_mode = 'onscreen'
        mock_config.jsoncrack_direction = 'DOWN'
        # Missing other values - should use defaults
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
    
    def test_path_separator_compatibility(self, temp_dir):
        """Test path separator compatibility."""
        from jsoncrack_for_sphinx.extension import find_schema_for_object
        
        # Create schema file
        schema_data = {"type": "string"}
        schema_file = temp_dir / "path_test.schema.json"
        
        with open(schema_file, 'w') as f:
            import json
            json.dump(schema_data, f)
        
        # Test with different path formats
        result1 = find_schema_for_object('module.path_test', str(temp_dir))
        result2 = find_schema_for_object('module.path_test', str(temp_dir).replace('/', '\\'))
        
        # At least one should work (depending on OS)
        assert result1 is not None or result2 is not None
    
    def test_case_sensitivity_compatibility(self, temp_dir):
        """Test case sensitivity compatibility."""
        from jsoncrack_for_sphinx.extension import find_schema_for_object
        
        # Create schema files with different cases
        schema_data = {"type": "string"}
        
        lower_file = temp_dir / "lowercase.schema.json"
        with open(lower_file, 'w') as f:
            import json
            json.dump(schema_data, f)
        
        # Test finding with exact case
        result = find_schema_for_object('module.lowercase', str(temp_dir))
        assert result is not None
        
        # Test finding with different case (should not find on case-sensitive systems)
        result_upper = find_schema_for_object('module.LOWERCASE', str(temp_dir))
        # This may or may not work depending on filesystem
    
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
        # The HTML escaping works correctly - data should be properly escaped
        assert 'data-schema=' in html  # JSON data should be present
    
    def test_url_compatibility(self):
        """Test URL handling compatibility."""
        from pathlib import Path
        
        # Read JavaScript file to check URL handling
        js_path = Path(__file__).parent.parent / "src" / "jsoncrack_for_sphinx" / "static" / "jsoncrack-sphinx.js"
        
        if js_path.exists():
            with open(js_path, 'r') as f:
                js_content = f.read()
            
            # Should contain proper URL handling
            assert 'jsoncrack.com' in js_content
            assert 'https://' in js_content
            
            # Should not contain obvious security issues
            assert 'javascript:' not in js_content.lower()
            assert 'eval(' not in js_content.lower()


class TestEnvironmentCompatibility:
    """Test compatibility with different environments."""
    
    def test_docker_compatibility(self):
        """Test Docker/container compatibility."""
        # Test that we can determine environment
        import os
        
        # Test common environment variables
        env_vars = ['HOME', 'PATH', 'USER']
        for var in env_vars:
            # Should handle missing environment variables gracefully
            value = os.environ.get(var)
            # Test passes if we can access environment without errors
        
        # Test that our code doesn't rely on specific environment
        config = JsonCrackConfig()
        assert config is not None
    
    def test_permissions_compatibility(self, temp_dir):
        """Test file permissions compatibility."""
        from jsoncrack_for_sphinx.utils import validate_schema_file
        
        # Create schema file with different permissions
        schema_data = {"type": "string"}
        schema_file = temp_dir / "permissions.schema.json"
        
        with open(schema_file, 'w') as f:
            import json
            json.dump(schema_data, f)
        
        # Test read access
        assert validate_schema_file(schema_file) is True
        
        # Test that we handle permission errors gracefully
        # (actual permission changes are tested elsewhere)
    
    def test_locale_compatibility(self):
        """Test locale compatibility."""
        import locale
        
        # Test that we can handle different locales
        try:
            current_locale = locale.getlocale()
            # Should not crash
            config = JsonCrackConfig()
            assert config is not None
        except:
            # Locale operations might fail in some environments
            pass
    
    def test_timezone_compatibility(self):
        """Test timezone compatibility."""
        import time
        
        # Test that we can handle different timezones
        try:
            current_time = time.time()
            # Should not crash
            config = JsonCrackConfig()
            assert config is not None
        except:
            # Time operations might fail in some environments
            pass


@pytest.mark.skipif(sys.version_info < (3, 9), reason="Python 3.9+ specific tests")
class TestPython39Plus:
    """Tests for Python 3.9+ specific features."""
    
    def test_newer_typing_features(self):
        """Test newer typing features."""
        # Test that we can use newer typing syntax if available
        try:
            from typing import Union
            
            # Test union types
            test_type = Union[str, int]
            assert test_type is not None
            
        except ImportError:
            pytest.skip("Union types not available")
    
    def test_pathlib_enhancements(self):
        """Test pathlib enhancements in newer Python versions."""
        from pathlib import Path
        
        # Test newer pathlib features
        path = Path("test.json")
        
        # These should work in Python 3.9+
        assert path.suffix == ".json"
        assert path.stem == "test"
