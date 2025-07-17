"""
Tests for the main extension module - fixed version.
"""

import json
import html
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock, PropertyMock

import pytest

from jsoncrack_for_sphinx.extension import (
    get_jsoncrack_config, SchemaDirective, find_schema_for_object,
    generate_schema_html, autodoc_process_signature, 
    autodoc_process_docstring, setup
)
from jsoncrack_for_sphinx.config import (
    JsonCrackConfig, RenderMode, Directions, Theme, 
    ContainerConfig, RenderConfig
)


class TestGetJsoncrackConfig:
    """Test getting JSONCrack configuration from app config."""
    
    def test_get_config_new_style(self):
        """Test getting new-style configuration."""
        app_config = Mock()
        app_config.jsoncrack_default_options = {
            'render': RenderConfig(RenderMode.OnLoad()),
            'container': ContainerConfig(
                direction=Directions.LEFT,
                height='600',
                width='90%'
            ),
            'theme': Theme.DARK
        }
        
        config = get_jsoncrack_config(app_config)
        
        assert isinstance(config.render.mode, RenderMode.OnLoad)
        assert config.container.direction == Directions.LEFT
        assert config.container.height == '600'
        assert config.container.width == '90%'
        assert config.theme == Theme.DARK
    
    def test_get_config_old_style(self):
        """Test getting old-style configuration."""
        app_config = Mock()
        # Remove new-style config
        delattr(app_config, 'jsoncrack_default_options') if hasattr(app_config, 'jsoncrack_default_options') else None
        
        # Set old-style config
        app_config.jsoncrack_render_mode = 'onscreen'
        app_config.jsoncrack_direction = 'TOP'
        app_config.jsoncrack_theme = 'light'
        app_config.jsoncrack_height = '700'
        app_config.jsoncrack_width = '80%'
        app_config.jsoncrack_onscreen_threshold = 0.3
        app_config.jsoncrack_onscreen_margin = '100px'
        
        config = get_jsoncrack_config(app_config)
        
        assert isinstance(config.render.mode, RenderMode.OnScreen)
        assert config.render.mode.threshold == 0.3
        assert config.render.mode.margin == '100px'
        assert config.container.direction == Directions.TOP
        assert config.container.height == '700'
        assert config.container.width == '80%'
        assert config.theme == Theme.LIGHT
    
    def test_get_config_old_style_defaults(self):
        """Test getting old-style configuration with default values."""
        app_config = Mock()
        delattr(app_config, 'jsoncrack_default_options') if hasattr(app_config, 'jsoncrack_default_options') else None
        
        # Set only some values, others should use defaults
        app_config.jsoncrack_render_mode = 'onclick'
        app_config.jsoncrack_direction = 'RIGHT'
        app_config.jsoncrack_theme = None
        app_config.jsoncrack_height = '500'
        app_config.jsoncrack_width = '100%'
        app_config.jsoncrack_onscreen_threshold = 0.1
        app_config.jsoncrack_onscreen_margin = '50px'
        
        config = get_jsoncrack_config(app_config)
        
        assert isinstance(config.render.mode, RenderMode.OnClick)
        assert config.container.direction == Directions.RIGHT
        assert config.theme == Theme.AUTO


class TestSchemaDirective:
    """Test the schema directive."""
    
    def test_schema_directive_creation(self, mock_sphinx_app):
        """Test creating a schema directive."""
        # Create mock environment
        mock_env = Mock()
        mock_env.config = Mock()
        mock_env.config.json_schema_dir = '/test/schemas'
        
        # Create mock state with env
        mock_state = Mock()
        mock_state.document = Mock()
        mock_state.document.settings = Mock()
        mock_state.document.settings.env = mock_env
        
        directive = SchemaDirective(
            name='schema',
            arguments=['User.create'],
            options={'title': 'Test Schema'},
            content=[],
            lineno=1,
            content_offset=0,
            block_text='',
            state=mock_state,
            state_machine=Mock()
        )
        
        assert directive.arguments == ['User.create']
        assert directive.options == {'title': 'Test Schema'}
        assert directive.env.config.json_schema_dir == '/test/schemas'
    
    def test_find_schema_file_found(self, schema_dir):
        """Test finding an existing schema file."""
        mock_state = Mock()
        mock_state.document = Mock()
        mock_state.document.settings = Mock()
        mock_state.document.settings.env = Mock()
        
        directive = SchemaDirective(
            name='schema',
            arguments=['User.create'],
            options={},
            content=[],
            lineno=1,
            content_offset=0,
            block_text='',
            state=mock_state,
            state_machine=Mock()
        )
        
        result = directive._find_schema_file('User.create', str(schema_dir))
        
        assert result is not None
        assert result.name == 'User.create.schema.json'
    
    def test_find_schema_file_not_found(self, schema_dir):
        """Test finding a non-existent schema file."""
        mock_state = Mock()
        mock_state.document = Mock()
        mock_state.document.settings = Mock()
        mock_state.document.settings.env = Mock()
        
        directive = SchemaDirective(
            name='schema',
            arguments=['NonExistent.method'],
            options={},
            content=[],
            lineno=1,
            content_offset=0,
            block_text='',
            state=mock_state,
            state_machine=Mock()
        )
        
        result = directive._find_schema_file('NonExistent.method', str(schema_dir))
        assert result is None
    
    def test_find_schema_file_no_schema_dir(self):
        """Test finding schema file when no schema directory is configured."""
        mock_state = Mock()
        mock_state.document = Mock()
        mock_state.document.settings = Mock()
        mock_state.document.settings.env = Mock()
        
        directive = SchemaDirective(
            name='schema',
            arguments=['User.create'],
            options={},
            content=[],
            lineno=1,
            content_offset=0,
            block_text='',
            state=mock_state,
            state_machine=Mock()
        )
        
        result = directive._find_schema_file('User.create', None)
        assert result is None
    
    def test_generate_schema_html_with_options(self, schema_dir):
        """Test generating schema HTML with directive options."""
        mock_env = Mock()
        mock_config = Mock()
        mock_config.jsoncrack_default_options = {}
        mock_env.config = mock_config
        
        mock_state = Mock()
        mock_state.document = Mock()
        mock_state.document.settings = Mock()
        mock_state.document.settings.env = mock_env
        
        directive = SchemaDirective(
            name='schema',
            arguments=['User.create'],
            options={
                'title': 'Custom Title',
                'description': 'Custom description',
                'render_mode': 'onload',
                'direction': 'LEFT',
                'height': '600'
            },
            content=[],
            lineno=1,
            content_offset=0,
            block_text='',
            state=mock_state,
            state_machine=Mock()
        )
        
        schema_path = schema_dir / 'User.create.schema.json'
        html_content = directive._generate_schema_html(schema_path)
        
        assert 'Custom Title' in html_content
        assert 'Custom description' in html_content
        assert 'jsoncrack-container' in html_content
        assert 'data-render-mode="onload"' in html_content
        assert 'data-direction="LEFT"' in html_content
        assert 'data-height="600"' in html_content


class TestFindSchemaForObject:
    """Test finding schema files for objects."""
    
    def test_find_schema_for_method(self, schema_dir):
        """Test finding schema for a method."""
        result = find_schema_for_object('example_module.User.create', str(schema_dir))
        
        assert result is not None
        schema_path, file_type = result
        assert Path(schema_path).name == 'User.create.schema.json'
        assert file_type == 'schema'
    
    def test_find_schema_for_function(self, schema_dir):
        """Test finding schema for a function."""
        result = find_schema_for_object('example_module.process_data', str(schema_dir))
        
        assert result is not None
        schema_path, file_type = result
        assert Path(schema_path).name == 'process_data.schema.json'
        assert file_type == 'schema'
    
    def test_find_json_for_method(self, schema_dir):
        """Test finding JSON data for a method."""
        result = find_schema_for_object('example_module.User.example', str(schema_dir))
        
        assert result is not None
        schema_path, file_type = result
        assert Path(schema_path).name == 'User.example.json'
        assert file_type == 'json'
    
    def test_find_schema_not_found(self, schema_dir):
        """Test finding schema for non-existent object."""
        result = find_schema_for_object('example_module.NonExistent.method', str(schema_dir))
        assert result is None
    
    def test_find_schema_no_schema_dir(self):
        """Test finding schema when no schema directory is configured."""
        result = find_schema_for_object('example_module.User.create', None)
        assert result is None
    
    def test_find_schema_non_existent_dir(self):
        """Test finding schema in non-existent directory."""
        result = find_schema_for_object('example_module.User.create', '/non/existent/dir')
        assert result is None
    
    def test_find_schema_priority_schema_over_json(self, temp_dir):
        """Test that .schema.json files have priority over .json files."""
        # Create both schema and json files
        schema_data = {"type": "object", "title": "Schema File"}
        json_data = {"example": "data"}
        
        schema_path = temp_dir / "User.method.schema.json"
        with open(schema_path, 'w') as f:
            json.dump(schema_data, f)
        
        json_path = temp_dir / "User.method.json"
        with open(json_path, 'w') as f:
            json.dump(json_data, f)
        
        result = find_schema_for_object('example_module.User.method', str(temp_dir))
        
        assert result is not None
        found_path, file_type = result
        assert Path(found_path).name == 'User.method.schema.json'
        assert file_type == 'schema'


class TestGenerateSchemaHtml:
    """Test generating schema HTML."""
    
    def test_generate_schema_html_schema_file(self, schema_file):
        """Test generating HTML for a schema file."""
        html_content = generate_schema_html(schema_file, 'schema')
        
        assert 'jsoncrack-container' in html_content
        assert 'data-schema=' in html_content
        assert 'data-render-mode="onclick"' in html_content
        assert 'data-direction="RIGHT"' in html_content
        assert 'data-height="500"' in html_content
        assert 'data-width="100%"' in html_content
    
    def test_generate_schema_html_json_file(self, json_file):
        """Test generating HTML for a JSON data file."""
        html_content = generate_schema_html(json_file, 'json')
        
        assert 'jsoncrack-container' in html_content
        assert 'data-schema=' in html_content
        # Should contain the actual JSON data
        assert 'John Doe' in html_content or 'john.doe@example.com' in html_content
    
    def test_generate_schema_html_with_config(self, schema_file):
        """Test generating HTML with custom configuration."""
        mock_config = Mock()
        mock_config.jsoncrack_default_options = {
            'render': RenderConfig(RenderMode.OnLoad()),
            'container': ContainerConfig(
                direction=Directions.LEFT,
                height='600',
                width='90%'
            ),
            'theme': Theme.DARK
        }
        
        html_content = generate_schema_html(schema_file, 'schema', mock_config)
        
        assert 'data-render-mode="onload"' in html_content
        assert 'data-direction="LEFT"' in html_content
        assert 'data-height="600"' in html_content
        assert 'data-width="90%"' in html_content
        assert 'data-theme="dark"' in html_content
    
    def test_generate_schema_html_invalid_file(self, temp_dir):
        """Test generating HTML for invalid schema file."""
        invalid_file = temp_dir / "invalid.schema.json"
        with open(invalid_file, 'w') as f:
            f.write("invalid json")
        
        html_content = generate_schema_html(invalid_file, 'schema')
        
        assert 'error' in html_content.lower()
        assert 'Error processing schema file' in html_content
    
    def test_generate_schema_html_with_jsf_available(self, schema_file):
        """Test generating HTML with JSF fake data generation when available."""
        # Mock JSF module import
        mock_jsf_module = Mock()
        mock_jsf_class = Mock()
        mock_jsf_instance = Mock()
        mock_jsf_instance.generate.return_value = {
            "name": "Fake Name",
            "email": "fake@example.com",
            "age": 25
        }
        mock_jsf_class.return_value = mock_jsf_instance
        mock_jsf_module.JSF = mock_jsf_class
        
        with patch.dict('sys.modules', {'jsf': mock_jsf_module}):
            html_content = generate_schema_html(schema_file, 'schema')
            
            assert 'jsoncrack-container' in html_content
            # Should contain the fake data
            assert 'Fake Name' in html_content or 'fake@example.com' in html_content
    
    def test_generate_schema_html_jsf_import_error(self, schema_file):
        """Test generating HTML when JSF is not available."""
        with patch('builtins.__import__', side_effect=ImportError("No module named 'jsf'")):
            html_content = generate_schema_html(schema_file, 'schema')
            
            # Should return error HTML when JSF import fails during schema processing
            assert 'error' in html_content.lower()
            assert 'Error processing schema file' in html_content
    
    def test_generate_schema_html_jsf_generation_error(self, schema_file):
        """Test generating HTML when JSF fails to generate data."""
        # Mock JSF module import but make generation fail
        mock_jsf_module = Mock()
        mock_jsf_class = Mock()
        mock_jsf_instance = Mock()
        mock_jsf_instance.generate.side_effect = Exception("JSF generation error")
        mock_jsf_class.return_value = mock_jsf_instance
        mock_jsf_module.JSF = mock_jsf_class
        
        with patch.dict('sys.modules', {'jsf': mock_jsf_module}):
            html_content = generate_schema_html(schema_file, 'schema')
            
            assert 'jsoncrack-container' in html_content
            # Should fall back to using the schema as-is
            assert 'data-schema=' in html_content


class TestAutodocProcessSignature:
    """Test autodoc signature processing."""
    
    def test_autodoc_process_signature_function(self, schema_dir):
        """Test processing signature for a function."""
        mock_app = Mock()
        mock_app.config = Mock()
        mock_app.config.json_schema_dir = str(schema_dir)
        mock_app.env = Mock()
        mock_app.env._jsoncrack_schema_paths = {}
        
        result = autodoc_process_signature(
            mock_app, 'function', 'example_module.process_data', 
            Mock(), {}, 'signature', 'return_annotation'
        )
        
        # Should return None (no modification to signature)
        assert result is None
        
        # Should store schema path in env
        assert hasattr(mock_app.env, '_jsoncrack_schema_paths')
        schema_paths = getattr(mock_app.env, '_jsoncrack_schema_paths')
        assert 'example_module.process_data' in schema_paths
    
    def test_autodoc_process_signature_method(self, schema_dir):
        """Test processing signature for a method."""
        mock_app = Mock()
        mock_app.config = Mock()
        mock_app.config.json_schema_dir = str(schema_dir)
        mock_app.env = Mock()
        mock_app.env._jsoncrack_schema_paths = {}
        
        result = autodoc_process_signature(
            mock_app, 'method', 'example_module.User.create', 
            Mock(), {}, 'signature', 'return_annotation'
        )
        
        assert result is None
        
        schema_paths = getattr(mock_app.env, '_jsoncrack_schema_paths')
        assert 'example_module.User.create' in schema_paths
    
    def test_autodoc_process_signature_no_schema_dir(self):
        """Test processing signature when no schema directory is configured."""
        mock_app = Mock()
        mock_app.config = Mock()
        mock_app.config.json_schema_dir = None
        mock_app.env = Mock()
        
        result = autodoc_process_signature(
            mock_app, 'function', 'example_module.process_data', 
            Mock(), {}, 'signature', 'return_annotation'
        )
        
        assert result is None
    
    def test_autodoc_process_signature_not_supported_type(self, schema_dir):
        """Test processing signature for unsupported object type."""
        mock_app = Mock()
        mock_app.config = Mock()
        mock_app.config.json_schema_dir = str(schema_dir)
        mock_app.env = Mock()
        
        result = autodoc_process_signature(
            mock_app, 'attribute', 'example_module.some_attr', 
            Mock(), {}, 'signature', 'return_annotation'
        )
        
        assert result is None
    
    def test_autodoc_process_signature_schema_not_found(self, schema_dir):
        """Test processing signature when schema is not found."""
        mock_app = Mock()
        mock_app.config = Mock()
        mock_app.config.json_schema_dir = str(schema_dir)
        mock_app.env = Mock()
        
        result = autodoc_process_signature(
            mock_app, 'function', 'example_module.non_existent_function', 
            Mock(), {}, 'signature', 'return_annotation'
        )
        
        assert result is None


class TestAutodocProcessDocstring:
    """Test autodoc docstring processing."""
    
    def test_autodoc_process_docstring_with_schema(self, schema_dir):
        """Test processing docstring with schema data."""
        mock_app = Mock()
        mock_app.config = Mock()
        mock_app.config.jsoncrack_default_options = {}
        mock_app.env = Mock()
        mock_app.env._jsoncrack_schema_paths = {
            'example_module.User.create': (str(schema_dir / 'User.create.schema.json'), 'schema')
        }
        
        lines = ['Function description', '', 'Args:', '    data: Input data']
        
        autodoc_process_docstring(
            mock_app, 'method', 'example_module.User.create', 
            Mock(), {}, lines
        )
        
        # Should add schema HTML to docstring
        assert len(lines) > 4
        assert any('.. raw:: html' in line for line in lines)
        assert any('jsoncrack-container' in line for line in lines)
    
    def test_autodoc_process_docstring_no_schema_paths(self):
        """Test processing docstring when no schema paths are stored."""
        mock_app = Mock()
        mock_app.config = Mock()
        mock_app.env = Mock()
        # Explicitly remove the _jsoncrack_schema_paths attribute
        if hasattr(mock_app.env, '_jsoncrack_schema_paths'):
            delattr(mock_app.env, '_jsoncrack_schema_paths')
        
        lines = ['Function description']
        original_lines = lines.copy()
        
        autodoc_process_docstring(
            mock_app, 'function', 'example_module.some_function', 
            Mock(), {}, lines
        )
        
        # Should not modify lines
        assert lines == original_lines
    
    def test_autodoc_process_docstring_no_matching_schema(self, schema_dir):
        """Test processing docstring when no matching schema is found."""
        mock_app = Mock()
        mock_app.config = Mock()
        mock_app.env = Mock()
        mock_app.env._jsoncrack_schema_paths = {
            'example_module.other_function': (str(schema_dir / 'other.schema.json'), 'schema')
        }
        
        lines = ['Function description']
        original_lines = lines.copy()
        
        autodoc_process_docstring(
            mock_app, 'function', 'example_module.some_function', 
            Mock(), {}, lines
        )
        
        # Should not modify lines
        assert lines == original_lines
    
    def test_autodoc_process_docstring_legacy_format(self, schema_dir):
        """Test processing docstring with legacy schema path format."""
        mock_app = Mock()
        mock_app.config = Mock()
        mock_app.env = Mock()
        mock_app.env._jsoncrack_schema_paths = {
            'example_module.User.create': str(schema_dir / 'User.create.schema.json')
        }
        
        lines = ['Function description']
        
        autodoc_process_docstring(
            mock_app, 'method', 'example_module.User.create', 
            Mock(), {}, lines
        )
        
        # Should add schema HTML to docstring
        assert len(lines) > 1
        assert any('.. raw:: html' in line for line in lines)
    
    def test_autodoc_process_docstring_unsupported_type(self, schema_dir):
        """Test processing docstring for unsupported object type."""
        mock_app = Mock()
        mock_app.config = Mock()
        mock_app.env = Mock()
        mock_app.env._jsoncrack_schema_paths = {
            'example_module.some_attr': (str(schema_dir / 'some.schema.json'), 'schema')
        }
        
        lines = ['Attribute description']
        original_lines = lines.copy()
        
        autodoc_process_docstring(
            mock_app, 'attribute', 'example_module.some_attr', 
            Mock(), {}, lines
        )
        
        # Should not modify lines
        assert lines == original_lines


class TestSetup:
    """Test the setup function."""
    
    def test_setup_function(self):
        """Test the setup function registers everything correctly."""
        mock_app = Mock()
        mock_app.config = Mock()
        mock_app.config.html_static_path = []
        
        result = setup(mock_app)
        
        # Should add config values
        assert mock_app.add_config_value.call_count >= 8
        
        # Should add directive
        mock_app.add_directive.assert_called_once_with('schema', SchemaDirective)
        
        # Should connect to autodoc events
        assert mock_app.connect.call_count >= 2
        
        # Should add CSS and JS files
        mock_app.add_css_file.assert_called_once_with('jsoncrack-schema.css')
        mock_app.add_js_file.assert_called_once_with('jsoncrack-sphinx.js')
        
        # Should return correct metadata
        assert result['version'] == '0.1.0'
        assert result['parallel_read_safe'] is True
        assert result['parallel_write_safe'] is True
    
    def test_setup_adds_static_path(self):
        """Test that setup adds static path to config."""
        mock_app = Mock()
        mock_app.config = Mock()
        mock_app.config.html_static_path = []
        
        setup(mock_app)
        
        # Should add static path
        assert len(mock_app.config.html_static_path) == 1
        assert 'static' in mock_app.config.html_static_path[0]
