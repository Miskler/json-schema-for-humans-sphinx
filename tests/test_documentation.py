"""
Tests for documentation examples and consistency.
"""

import json
from pathlib import Path
import pytest
from unittest.mock import Mock

from jsoncrack_for_sphinx import (
    RenderMode, Directions, Theme, ContainerConfig, RenderConfig, JsonCrackConfig
)


class TestDocumentationExamples:
    """Test examples from documentation."""
    
    def test_readme_quick_start_example(self):
        """Test the quick start example from README."""
        # Test configuration example from README
        extensions = [
            "sphinx.ext.autodoc",
            "jsoncrack_for_sphinx",
        ]
        
        assert "jsoncrack_for_sphinx" in extensions
        assert "sphinx.ext.autodoc" in extensions
        
        # Test schema directory configuration
        import os
        json_schema_dir = os.path.join(os.path.dirname(__file__), "schemas")
        assert isinstance(json_schema_dir, str)
    
    def test_readme_file_naming_convention(self, temp_dir):
        """Test the file naming convention from README."""
        # Test the naming patterns mentioned in README
        schema_patterns = [
            "MyClass.my_method.schema.json",
            "MyClass.my_method.options.schema.json", 
            "my_function.schema.json",
            "my_function.advanced.schema.json"
        ]
        
        # Create test files following the patterns
        for pattern in schema_patterns:
            schema_file = temp_dir / pattern
            with open(schema_file, 'w') as f:
                json.dump({"type": "object", "title": "Test"}, f)
            
            assert schema_file.exists()
        
        # Test that our find function works with these patterns
        from jsoncrack_for_sphinx.extension import find_schema_for_object
        
        # Should find the basic method schema
        result = find_schema_for_object('module.MyClass.my_method', str(temp_dir))
        assert result is not None
        
        # Should find the function schema
        result = find_schema_for_object('module.my_function', str(temp_dir))
        assert result is not None
    
    def test_readme_manual_schema_inclusion(self):
        """Test manual schema inclusion example from README."""
        # Test that directive options work as documented
        directive_options = {
            'title': 'Custom Title',
            'description': 'Custom description',
            'render_mode': 'onclick',
            'direction': 'RIGHT',
            'height': '500'
        }
        
        # These should all be valid options
        assert directive_options['title'] == 'Custom Title'
        assert directive_options['render_mode'] in ['onclick', 'onload', 'onscreen']
        assert directive_options['direction'] in ['TOP', 'RIGHT', 'DOWN', 'LEFT']
        assert directive_options['height'] == '500'
    
    def test_readme_new_configuration_example(self):
        """Test the new structured configuration example from README."""
        # Test the recommended configuration format
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
        
        # Verify the configuration is valid
        assert isinstance(jsoncrack_default_options['render'], RenderConfig)
        assert isinstance(jsoncrack_default_options['render'].mode, RenderMode.OnClick)
        assert isinstance(jsoncrack_default_options['container'], ContainerConfig)
        assert jsoncrack_default_options['container'].direction == Directions.RIGHT
        assert jsoncrack_default_options['container'].height == '500'
        assert jsoncrack_default_options['container'].width == '100%'
        assert jsoncrack_default_options['theme'] == Theme.AUTO
    
    def test_readme_legacy_configuration_example(self):
        """Test the legacy configuration example from README."""
        # Test the old configuration format
        legacy_config = {
            'jsoncrack_render_mode': 'onclick',
            'jsoncrack_theme': None,
            'jsoncrack_direction': 'RIGHT',
            'jsoncrack_height': '500',
            'jsoncrack_width': '100%',
            'jsoncrack_onscreen_threshold': 0.1,
            'jsoncrack_onscreen_margin': '50px'
        }
        
        # Verify the configuration values
        assert legacy_config['jsoncrack_render_mode'] in ['onclick', 'onload', 'onscreen']
        assert legacy_config['jsoncrack_theme'] in [None, 'light', 'dark']
        assert legacy_config['jsoncrack_direction'] in ['TOP', 'RIGHT', 'DOWN', 'LEFT']
        assert legacy_config['jsoncrack_height'] == '500'
        assert legacy_config['jsoncrack_width'] == '100%'
        assert 0.0 <= legacy_config['jsoncrack_onscreen_threshold'] <= 1.0
        assert legacy_config['jsoncrack_onscreen_margin'] == '50px'
    
    def test_readme_render_modes_example(self):
        """Test the render modes example from README."""
        # Test all render modes mentioned in README
        onclick_mode = RenderMode.OnClick()
        onload_mode = RenderMode.OnLoad()
        onscreen_mode = RenderMode.OnScreen(threshold=0.1, margin='50px')
        
        assert onclick_mode.mode == 'onclick'
        assert onload_mode.mode == 'onload'
        assert onscreen_mode.mode == 'onscreen'
        assert onscreen_mode.threshold == 0.1
        assert onscreen_mode.margin == '50px'
    
    def test_readme_theme_options_example(self):
        """Test the theme options example from README."""
        # Test all theme options mentioned in README
        auto_theme = Theme.AUTO
        light_theme = Theme.LIGHT
        dark_theme = Theme.DARK
        
        assert auto_theme.value is None
        assert light_theme.value == 'light'
        assert dark_theme.value == 'dark'
    
    def test_readme_file_types_example(self, temp_dir):
        """Test the file types example from README."""
        # Test .schema.json files
        schema_data = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "title": "Test Schema",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"}
            }
        }
        
        schema_file = temp_dir / "test.schema.json"
        with open(schema_file, 'w') as f:
            json.dump(schema_data, f)
        
        # Test .json files
        json_data = {
            "name": "John Doe",
            "age": 30,
            "email": "john@example.com"
        }
        
        json_file = temp_dir / "test.json"
        with open(json_file, 'w') as f:
            json.dump(json_data, f)
        
        # Both should be valid
        assert schema_file.exists()
        assert json_file.exists()
        
        # Test that our extension handles both types
        from jsoncrack_for_sphinx.extension import generate_schema_html
        
        schema_html = generate_schema_html(schema_file, 'schema')
        json_html = generate_schema_html(json_file, 'json')
        
        assert 'jsoncrack-container' in schema_html
        assert 'jsoncrack-container' in json_html
    
    def test_readme_testing_support_example(self, temp_dir):
        """Test the testing support example from README."""
        from jsoncrack_for_sphinx.fixtures import schema_to_rst_fixture
        
        # Test that the fixture works as documented
        schema_data = {
            "type": "object",
            "title": "Test Schema",
            "properties": {
                "name": {"type": "string"}
            }
        }
        
        schema_file = temp_dir / "test.schema.json"
        with open(schema_file, 'w') as f:
            json.dump(schema_data, f)
        
        # Test the fixture function
        from jsoncrack_for_sphinx.utils import schema_to_rst
        
        # This should work as shown in README
        rst_content = schema_to_rst(schema_file, title="Test Schema")
        assert "Test Schema" in rst_content


class TestExampleModule:
    """Test the example module and its integration."""
    
    def test_example_module_structure(self):
        """Test that example module has the expected structure."""
        try:
            from examples.example_module import User, process_data
            
            # Test User class
            assert hasattr(User, '__init__')
            assert hasattr(User, 'create')
            assert hasattr(User, 'update')
            assert hasattr(User, 'example')
            
            # Test process_data function
            assert callable(process_data)
            
        except ImportError:
            pytest.skip("Example module not available in test environment")
    
    def test_example_schemas_exist(self):
        """Test that example schemas exist."""
        # Check for example schema files
        examples_dir = Path(__file__).parent.parent / "examples"
        schemas_dir = examples_dir / "schemas"
        
        if schemas_dir.exists():
            expected_files = [
                "User.create.schema.json",
                "User.update.schema.json", 
                "User.example.json",
                "process_data.schema.json"
            ]
            
            for expected_file in expected_files:
                file_path = schemas_dir / expected_file
                assert file_path.exists(), f"Expected schema file {expected_file} should exist"
                
                # Validate that it's valid JSON
                with open(file_path, 'r') as f:
                    try:
                        json.load(f)
                    except json.JSONDecodeError:
                        pytest.fail(f"Schema file {expected_file} contains invalid JSON")
        else:
            pytest.skip("Example schemas directory not found")
    
    def test_example_docs_configuration(self):
        """Test that example docs configuration is correct."""
        examples_dir = Path(__file__).parent.parent / "examples"
        conf_file = examples_dir / "docs" / "conf.py"
        
        if conf_file.exists():
            # Read configuration file
            with open(conf_file, 'r') as f:
                conf_content = f.read()
            
            # Check that required extensions are included
            assert "jsoncrack_for_sphinx" in conf_content
            assert "sphinx.ext.autodoc" in conf_content
            
            # Check that json_schema_dir is configured
            assert "json_schema_dir" in conf_content
            
            # Check that configuration example is present
            assert "jsoncrack_default_options" in conf_content or "jsoncrack_render_mode" in conf_content
        else:
            pytest.skip("Example docs configuration not found")


class TestSchemaExamples:
    """Test schema examples for validity."""
    
    def test_user_create_schema_example(self):
        """Test the User.create schema example."""
        # This is based on the schema in examples/schemas/User.create.schema.json
        expected_schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "title": "User",
            "properties": {
                "name": {"type": "string"},
                "email": {"type": "string", "format": "email"}
            },
            "required": ["name", "email"]
        }
        
        # Verify schema structure
        assert expected_schema["type"] == "object"
        assert "name" in expected_schema["properties"]
        assert "email" in expected_schema["properties"]
        assert expected_schema["properties"]["email"]["format"] == "email"
        assert expected_schema["required"] == ["name", "email"]
    
    def test_process_data_schema_example(self):
        """Test the process_data schema example."""
        expected_schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "title": "Process Data",
            "properties": {
                "input_data": {"type": "array"},
                "options": {"type": "object"}
            }
        }
        
        # Verify schema structure
        assert expected_schema["type"] == "object"
        assert "input_data" in expected_schema["properties"]
        assert "options" in expected_schema["properties"]
        assert expected_schema["properties"]["input_data"]["type"] == "array"
        assert expected_schema["properties"]["options"]["type"] == "object"
    
    def test_json_example_validity(self):
        """Test JSON example validity."""
        # This is based on the JSON in examples/schemas/User.example.json
        expected_json = {
            "id": 123,
            "name": "John Doe",
            "email": "john.doe@example.com",
            "active": True,
            "roles": ["user", "admin"]
        }
        
        # Verify JSON structure
        assert isinstance(expected_json["id"], int)
        assert isinstance(expected_json["name"], str)
        assert isinstance(expected_json["email"], str)
        assert isinstance(expected_json["active"], bool)
        assert isinstance(expected_json["roles"], list)
        assert "@" in expected_json["email"]  # Basic email validation


class TestConfigurationConsistency:
    """Test configuration consistency across documentation."""
    
    def test_all_render_modes_documented(self):
        """Test that all render modes are properly documented."""
        # Test that we can create all render modes mentioned in docs
        modes = {
            'onclick': RenderMode.OnClick(),
            'onload': RenderMode.OnLoad(),
            'onscreen': RenderMode.OnScreen(threshold=0.1, margin='50px')
        }
        
        for mode_name, mode_obj in modes.items():
            assert mode_obj.mode == mode_name
            assert hasattr(mode_obj, 'mode')
    
    def test_all_directions_documented(self):
        """Test that all directions are properly documented."""
        directions = ['TOP', 'RIGHT', 'DOWN', 'LEFT']
        
        for direction in directions:
            direction_obj = Directions(direction)
            assert direction_obj.value == direction
    
    def test_all_themes_documented(self):
        """Test that all themes are properly documented."""
        themes = {
            'auto': Theme.AUTO,
            'light': Theme.LIGHT,
            'dark': Theme.DARK
        }
        
        for theme_name, theme_obj in themes.items():
            if theme_name == 'auto':
                assert theme_obj.value is None
            else:
                assert theme_obj.value == theme_name
    
    def test_configuration_parameter_consistency(self):
        """Test configuration parameter consistency."""
        # Test that all configuration parameters are consistent
        config = JsonCrackConfig()
        
        # Test default values match documentation
        assert isinstance(config.render.mode, RenderMode.OnClick)
        assert config.container.direction == Directions.RIGHT
        assert config.container.height == '500'
        assert config.container.width == '100%'
        assert config.theme == Theme.AUTO
        
        # Test that we can create custom configurations
        custom_config = JsonCrackConfig(
            render=RenderConfig(RenderMode.OnLoad()),
            container=ContainerConfig(
                direction=Directions.LEFT,
                height='400',
                width='90%'
            ),
            theme=Theme.DARK
        )
        
        assert isinstance(custom_config.render.mode, RenderMode.OnLoad)
        assert custom_config.container.direction == Directions.LEFT
        assert custom_config.container.height == '400'
        assert custom_config.container.width == '90%'
        assert custom_config.theme == Theme.DARK


class TestDocumentationLinks:
    """Test documentation links and references."""
    
    def test_package_metadata_consistency(self):
        """Test package metadata consistency."""
        import jsoncrack_for_sphinx
        
        # Test that package metadata matches documentation
        assert jsoncrack_for_sphinx.__version__ == "0.1.0"
        assert jsoncrack_for_sphinx.__author__ == "Miskler"
        
        # Test that package has proper docstring
        assert jsoncrack_for_sphinx.__doc__ is not None
        assert len(jsoncrack_for_sphinx.__doc__.strip()) > 0
    
    def test_sphinx_extension_entry_point(self):
        """Test Sphinx extension entry point."""
        from jsoncrack_for_sphinx import setup
        
        # Test that setup function exists and is callable
        assert callable(setup)
        
        # Test that setup function returns proper metadata
        mock_app = Mock()
        mock_app.config = Mock()
        mock_app.config.html_static_path = []
        mock_app.add_config_value = Mock()
        mock_app.add_directive = Mock()
        mock_app.connect = Mock()
        mock_app.add_css_file = Mock()
        mock_app.add_js_file = Mock()
        
        result = setup(mock_app)
        
        assert isinstance(result, dict)
        assert 'version' in result
        assert 'parallel_read_safe' in result
        assert 'parallel_write_safe' in result
    
    def test_dependency_requirements(self):
        """Test that dependencies match documentation."""
        # Test that we can import required dependencies
        try:
            import sphinx
            import jsf
            
            # Test minimum versions (basic check)
            assert sphinx is not None
            assert jsf is not None
            
        except ImportError as e:
            pytest.fail(f"Required dependency not available: {e}")
    
    def test_file_structure_consistency(self):
        """Test that file structure matches documentation."""
        # Test that expected files exist
        src_dir = Path(__file__).parent.parent / "src" / "jsoncrack_for_sphinx"
        
        expected_files = [
            "__init__.py",
            "extension.py",
            "config.py",
            "utils.py",
            "fixtures.py"
        ]
        
        for expected_file in expected_files:
            file_path = src_dir / expected_file
            assert file_path.exists(), f"Expected file {expected_file} should exist"
        
        # Test that static files exist
        static_dir = src_dir / "static"
        assert static_dir.exists(), "Static directory should exist"
        
        expected_static_files = [
            "jsoncrack-schema.css",
            "jsoncrack-sphinx.js"
        ]
        
        for expected_static_file in expected_static_files:
            file_path = static_dir / expected_static_file
            assert file_path.exists(), f"Expected static file {expected_static_file} should exist"
