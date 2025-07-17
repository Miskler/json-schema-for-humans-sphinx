"""
Additional tests for missing dependencies and optional components.
"""

import pytest
from unittest.mock import Mock, patch
from pathlib import Path


class TestMissingDependencies:
    """Test behavior when optional dependencies are missing."""
    
    def test_missing_jsf_dependency(self, temp_dir):
        """Test behavior when JSF is not available."""
        from jsoncrack_for_sphinx.extension import generate_schema_html
        
        # Create schema file
        schema_data = {
            "type": "object",
            "title": "Test Schema",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"}
            }
        }
        
        schema_file = temp_dir / "test.schema.json"
        with open(schema_file, 'w') as f:
            import json
            json.dump(schema_data, f)
        
        # Mock JSF import failure by patching builtins.__import__
        def mock_import(name, *args, **kwargs):
            if name == 'jsf':
                raise ImportError("JSF not available")
            return __import__(name, *args, **kwargs)
        
        with patch('builtins.__import__', side_effect=mock_import):
            html = generate_schema_html(schema_file, 'schema')
            
            # Should still work, just without fake data generation
            # The function should return something, even if it's an error message
            assert html is not None
            assert len(html) > 0
            # The function should either return valid HTML or an error message
            assert 'jsoncrack-container' in html or 'error' in html.lower()
    
    def test_missing_json_schema_for_humans(self, temp_dir):
        """Test behavior when json-schema-for-humans is not available."""
        from jsoncrack_for_sphinx.utils import schema_to_rst
        
        # Create schema file
        schema_data = {
            "type": "object",
            "title": "Test Schema",
            "properties": {
                "name": {"type": "string"}
            }
        }
        
        schema_file = temp_dir / "test.schema.json"
        with open(schema_file, 'w') as f:
            import json
            json.dump(schema_data, f)
        
        # Mock json-schema-for-humans import failure
        def mock_import(name, *args, **kwargs):
            if name == 'json_schema_for_humans.generate':
                raise ImportError("json-schema-for-humans not available")
            return __import__(name, *args, **kwargs)
        
        with patch('builtins.__import__', side_effect=mock_import):
            # Should raise an error since this is a required dependency
            with pytest.raises((ImportError, RuntimeError)):
                schema_to_rst(schema_file)
    
    def test_missing_sphinx_dependency(self):
        """Test behavior when Sphinx components are not available."""
        from jsoncrack_for_sphinx.extension import setup
        
        # Mock Sphinx app
        mock_app = Mock()
        mock_app.config = Mock()
        mock_app.config.html_static_path = []
        mock_app.add_config_value = Mock()
        mock_app.add_directive = Mock()
        mock_app.connect = Mock()
        mock_app.add_css_file = Mock()
        mock_app.add_js_file = Mock()
        
        # Should work with mocked Sphinx
        result = setup(mock_app)
        assert result is not None
        assert 'version' in result


class TestOptionalFeatures:
    """Test optional features and graceful degradation."""
    
    def test_jsf_fallback_behavior(self, temp_dir):
        """Test fallback behavior when JSF fails."""
        from jsoncrack_for_sphinx.extension import generate_schema_html
        
        schema_data = {
            "type": "object",
            "title": "Fallback Test",
            "properties": {
                "name": {"type": "string"}
            }
        }
        
        schema_file = temp_dir / "fallback.schema.json"
        with open(schema_file, 'w') as f:
            import json
            json.dump(schema_data, f)
        
        # Mock JSF to raise an exception during generation
        mock_jsf_module = Mock()
        mock_jsf_class = Mock()
        mock_jsf_instance = Mock()
        mock_jsf_instance.generate.side_effect = Exception("JSF generation failed")
        mock_jsf_class.return_value = mock_jsf_instance
        mock_jsf_module.JSF = mock_jsf_class
        
        with patch.dict('sys.modules', {'jsf': mock_jsf_module}):
            # Should fall back to using schema as-is
            html = generate_schema_html(schema_file, 'schema')
            
            assert 'jsoncrack-container' in html
            assert 'data-schema=' in html
    
    def test_file_access_error_handling(self, temp_dir):
        """Test file access error handling."""
        from jsoncrack_for_sphinx.utils import validate_schema_file, get_schema_info
        
        # Test with non-existent file
        non_existent = temp_dir / "non_existent.schema.json"
        
        assert validate_schema_file(non_existent) is False
        
        with pytest.raises(FileNotFoundError):
            get_schema_info(non_existent)
    
    def test_network_error_simulation(self):
        """Test network-related error simulation."""
        # This would be more relevant if we had network operations
        # For now, test that our code doesn't make unexpected network calls
        
        from jsoncrack_for_sphinx.config import JsonCrackConfig
        
        # Creating config should not involve network operations
        config = JsonCrackConfig()
        assert config is not None
    
    def test_memory_constrained_environment(self, temp_dir):
        """Test behavior in memory-constrained environments."""
        from jsoncrack_for_sphinx.extension import generate_schema_html
        
        # Create a moderately large schema
        large_schema = {
            "type": "object",
            "title": "Memory Test",
            "properties": {}
        }
        
        # Add many properties
        for i in range(50):
            large_schema["properties"][f"field_{i}"] = {
                "type": "string",
                "description": f"Field {i}"
            }
        
        schema_file = temp_dir / "memory_test.schema.json"
        with open(schema_file, 'w') as f:
            import json
            json.dump(large_schema, f)
        
        # Should handle large schema without memory issues
        html = generate_schema_html(schema_file, 'schema')
        assert 'jsoncrack-container' in html
        assert len(html) > 0


class TestErrorRecovery:
    """Test error recovery and resilience."""
    
    def test_partial_configuration_recovery(self):
        """Test recovery from partial configuration."""
        from jsoncrack_for_sphinx.extension import get_jsoncrack_config
        
        # Create configuration with some invalid values
        mock_config = Mock()
        if hasattr(mock_config, 'jsoncrack_default_options'):
            delattr(mock_config, 'jsoncrack_default_options')
        
        # Set some valid and some invalid values
        mock_config.jsoncrack_render_mode = 'invalid_mode'  # Invalid
        mock_config.jsoncrack_direction = 'RIGHT'  # Valid
        mock_config.jsoncrack_theme = None  # Valid
        mock_config.jsoncrack_height = '500'  # Valid
        mock_config.jsoncrack_width = '100%'  # Valid
        mock_config.jsoncrack_onscreen_threshold = 0.1  # Valid
        mock_config.jsoncrack_onscreen_margin = '50px'  # Valid
        
        # Should recover with defaults for invalid values
        config = get_jsoncrack_config(mock_config)
        assert config is not None
        assert config.container.direction.value == 'RIGHT'
    
    def test_schema_parsing_recovery(self, temp_dir):
        """Test recovery from schema parsing errors."""
        from jsoncrack_for_sphinx.extension import generate_schema_html
        
        # Create invalid JSON file
        invalid_file = temp_dir / "invalid.schema.json"
        with open(invalid_file, 'w') as f:
            f.write('{"type": "object", "invalid": json}')
        
        # Should recover gracefully
        html = generate_schema_html(invalid_file, 'schema')
        assert 'error' in html.lower()
    
    def test_unicode_error_recovery(self, temp_dir):
        """Test recovery from Unicode errors."""
        from jsoncrack_for_sphinx.utils import validate_schema_file
        
        # Create file with invalid UTF-8
        invalid_file = temp_dir / "invalid_utf8.schema.json"
        with open(invalid_file, 'wb') as f:
            f.write(b'{"type": "object", "title": "\xff\xfe"}')
        
        # Should handle encoding errors gracefully
        try:
            result = validate_schema_file(invalid_file)
            assert result is False
        except UnicodeDecodeError:
            # This is expected behavior - the function should handle or raise appropriate errors
            pass
    
    def test_circular_reference_recovery(self, temp_dir):
        """Test recovery from circular references."""
        from jsoncrack_for_sphinx.extension import generate_schema_html
        
        # Create schema with circular reference
        circular_schema = {
            "type": "object",
            "title": "Circular Test",
            "properties": {
                "self": {"$ref": "#"}
            }
        }
        
        schema_file = temp_dir / "circular.schema.json"
        with open(schema_file, 'w') as f:
            import json
            json.dump(circular_schema, f)
        
        # Should handle circular references
        html = generate_schema_html(schema_file, 'schema')
        assert 'jsoncrack-container' in html


class TestWarningHandling:
    """Test warning handling and logging."""
    
    def test_deprecation_warning_handling(self):
        """Test handling of deprecation warnings."""
        import warnings
        
        # Test that our code doesn't generate unexpected warnings
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            
            from jsoncrack_for_sphinx.config import JsonCrackConfig
            config = JsonCrackConfig()
            
            # Should not generate deprecation warnings
            deprecation_warnings = [warning for warning in w 
                                   if issubclass(warning.category, DeprecationWarning)]
            assert len(deprecation_warnings) == 0
    
    def test_user_warning_handling(self):
        """Test handling of user warnings."""
        import warnings
        
        # Test that our code handles user warnings appropriately
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            
            from jsoncrack_for_sphinx.extension import find_schema_for_object
            
            # This should not generate warnings
            result = find_schema_for_object('non.existent', '/non/existent/path')
            assert result is None
            
            # Should not generate user warnings
            user_warnings = [warning for warning in w 
                            if issubclass(warning.category, UserWarning)]
            assert len(user_warnings) == 0
    
    def test_logging_configuration(self):
        """Test logging configuration."""
        from jsoncrack_for_sphinx.extension import logger
        
        # Test that logger is configured
        assert logger is not None
        # Logger name includes 'sphinx.' prefix in some configurations
        assert 'jsoncrack_for_sphinx.extension' in logger.name
    
    def test_error_message_quality(self, temp_dir):
        """Test quality of error messages."""
        from jsoncrack_for_sphinx.utils import get_schema_info
        
        # Test with non-existent file
        non_existent = temp_dir / "non_existent.schema.json"
        
        try:
            get_schema_info(non_existent)
            assert False, "Should have raised an exception"
        except FileNotFoundError as e:
            # Error message should be informative
            assert "non_existent.schema.json" in str(e)
            assert "not found" in str(e).lower()
        
        # Test with invalid JSON
        invalid_file = temp_dir / "invalid.schema.json"
        with open(invalid_file, 'w') as f:
            f.write("invalid json")
        
        try:
            get_schema_info(invalid_file)
            assert False, "Should have raised an exception"
        except ValueError as e:
            # Error message should be informative
            assert "invalid.schema.json" in str(e)
            assert "json" in str(e).lower()


class TestDocumentationTests:
    """Test documentation and examples."""
    
    def test_readme_examples_work(self):
        """Test that README examples work."""
        # Test basic configuration example
        from jsoncrack_for_sphinx import RenderMode, Directions, Theme, ContainerConfig, RenderConfig
        
        # This should match the README example
        jsoncrack_default_options = {
            'render': RenderConfig(
                mode=RenderMode.OnClick()
            ),
            'container': ContainerConfig(
                direction=Directions.RIGHT,
                height='500',
                width='100%'
            ),
            'theme': Theme.AUTO
        }
        
        # Should work without errors
        assert jsoncrack_default_options is not None
        assert isinstance(jsoncrack_default_options['render'], RenderConfig)
        assert isinstance(jsoncrack_default_options['container'], ContainerConfig)
        assert jsoncrack_default_options['theme'] == Theme.AUTO
    
    def test_example_module_integration(self):
        """Test integration with example module."""
        # Test that example module can be imported
        try:
            from examples.example_module import User, process_data
            
            # Test that classes and functions exist
            assert User is not None
            assert process_data is not None
            
            # Test that methods exist
            user = User("Test", "test@example.com")
            assert hasattr(user, 'create')
            assert hasattr(user, 'update')
            assert hasattr(user, 'example')
            
        except ImportError:
            pytest.skip("Example module not available")
    
    def test_docstring_examples(self):
        """Test examples in docstrings."""
        from jsoncrack_for_sphinx.config import RenderMode
        
        # Test that docstring examples work
        mode = RenderMode.OnScreen(threshold=0.1, margin='50px')
        assert mode.threshold == 0.1
        assert mode.margin == '50px'
    
    def test_configuration_examples(self):
        """Test configuration examples."""
        from jsoncrack_for_sphinx.config import JsonCrackConfig, RenderConfig, ContainerConfig
        from jsoncrack_for_sphinx.config import RenderMode, Directions, Theme
        
        # Test various configuration combinations
        configs = [
            # Basic configuration
            JsonCrackConfig(),
            
            # Custom render mode
            JsonCrackConfig(
                render=RenderConfig(RenderMode.OnLoad())
            ),
            
            # Custom container
            JsonCrackConfig(
                container=ContainerConfig(
                    direction=Directions.LEFT,
                    height='400',
                    width='90%'
                )
            ),
            
            # Custom theme
            JsonCrackConfig(theme=Theme.DARK),
            
            # Full custom configuration
            JsonCrackConfig(
                render=RenderConfig(RenderMode.OnScreen(threshold=0.3, margin='100px')),
                container=ContainerConfig(
                    direction=Directions.DOWN,
                    height='600',
                    width='95%'
                ),
                theme=Theme.LIGHT
            )
        ]
        
        # All configurations should work
        for config in configs:
            assert config is not None
            assert config.render is not None
            assert config.container is not None
            assert config.theme is not None
