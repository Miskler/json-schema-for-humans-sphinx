"""
Tests for the configuration module.
"""

import pytest
from unittest.mock import Mock

from jsoncrack_for_sphinx.config import (
    RenderMode, Directions, Theme, ContainerConfig, RenderConfig, 
    JsonCrackConfig, parse_config, get_config_values
)


class TestRenderMode:
    """Test render mode classes."""
    
    def test_onclick_mode(self):
        """Test OnClick render mode."""
        mode = RenderMode.OnClick()
        assert mode.mode == 'onclick'
        assert repr(mode) == "RenderMode.OnClick()"
    
    def test_onload_mode(self):
        """Test OnLoad render mode."""
        mode = RenderMode.OnLoad()
        assert mode.mode == 'onload'
        assert repr(mode) == "RenderMode.OnLoad()"
    
    def test_onscreen_mode_default(self):
        """Test OnScreen render mode with default values."""
        mode = RenderMode.OnScreen()
        assert mode.mode == 'onscreen'
        assert mode.threshold == 0.1
        assert mode.margin == '50px'
        assert repr(mode) == "RenderMode.OnScreen(threshold=0.1, margin='50px')"
    
    def test_onscreen_mode_custom(self):
        """Test OnScreen render mode with custom values."""
        mode = RenderMode.OnScreen(threshold=0.3, margin='100px')
        assert mode.mode == 'onscreen'
        assert mode.threshold == 0.3
        assert mode.margin == '100px'
        assert repr(mode) == "RenderMode.OnScreen(threshold=0.3, margin='100px')"


class TestDirections:
    """Test direction enum."""
    
    def test_direction_values(self):
        """Test all direction values."""
        assert Directions.TOP.value == 'TOP'
        assert Directions.RIGHT.value == 'RIGHT'
        assert Directions.DOWN.value == 'DOWN'
        assert Directions.LEFT.value == 'LEFT'


class TestTheme:
    """Test theme enum."""
    
    def test_theme_values(self):
        """Test all theme values."""
        assert Theme.LIGHT.value == 'light'
        assert Theme.DARK.value == 'dark'
        assert Theme.AUTO.value is None


class TestContainerConfig:
    """Test container configuration."""
    
    def test_default_container_config(self):
        """Test default container configuration."""
        config = ContainerConfig()
        assert config.direction == Directions.RIGHT
        assert config.height == '500'
        assert config.width == '100%'
        assert 'RIGHT' in repr(config)
        assert 'height' in repr(config)
    
    def test_custom_container_config(self):
        """Test custom container configuration."""
        config = ContainerConfig(
            direction=Directions.LEFT,
            height=400,
            width='80%'
        )
        assert config.direction == Directions.LEFT
        assert config.height == '400'
        assert config.width == '80%'
    
    def test_container_config_int_values(self):
        """Test container configuration with integer values."""
        config = ContainerConfig(height=600, width=800)
        assert config.height == '600'
        assert config.width == '800'


class TestRenderConfig:
    """Test render configuration."""
    
    def test_render_config_onclick(self):
        """Test render configuration with OnClick mode."""
        mode = RenderMode.OnClick()
        config = RenderConfig(mode)
        assert config.mode == mode
        assert 'OnClick' in repr(config)
    
    def test_render_config_onload(self):
        """Test render configuration with OnLoad mode."""
        mode = RenderMode.OnLoad()
        config = RenderConfig(mode)
        assert config.mode == mode
        assert 'OnLoad' in repr(config)
    
    def test_render_config_onscreen(self):
        """Test render configuration with OnScreen mode."""
        mode = RenderMode.OnScreen(threshold=0.2, margin='75px')
        config = RenderConfig(mode)
        assert config.mode == mode
        assert 'OnScreen' in repr(config)


class TestJsonCrackConfig:
    """Test main JSONCrack configuration."""
    
    def test_default_config(self):
        """Test default configuration."""
        config = JsonCrackConfig()
        assert isinstance(config.render.mode, RenderMode.OnClick)
        assert config.container.direction == Directions.RIGHT
        assert config.container.height == '500'
        assert config.container.width == '100%'
        assert config.theme == Theme.AUTO
    
    def test_custom_config(self):
        """Test custom configuration."""
        render_config = RenderConfig(RenderMode.OnLoad())
        container_config = ContainerConfig(
            direction=Directions.DOWN,
            height='400',
            width='90%'
        )
        
        config = JsonCrackConfig(
            render=render_config,
            container=container_config,
            theme=Theme.DARK
        )
        
        assert config.render == render_config
        assert config.container == container_config
        assert config.theme == Theme.DARK
    
    def test_config_with_none_values(self):
        """Test configuration with None values (should use defaults)."""
        config = JsonCrackConfig(render=None, container=None)
        assert isinstance(config.render.mode, RenderMode.OnClick)
        assert config.container.direction == Directions.RIGHT


class TestParseConfig:
    """Test configuration parsing."""
    
    def test_parse_empty_config(self):
        """Test parsing empty configuration."""
        config = parse_config({})
        assert isinstance(config.render.mode, RenderMode.OnClick)
        assert config.container.direction == Directions.RIGHT
        assert config.theme == Theme.AUTO
    
    def test_parse_full_config(self):
        """Test parsing full configuration."""
        config_dict = {
            'render': RenderConfig(RenderMode.OnLoad()),
            'container': ContainerConfig(
                direction=Directions.LEFT,
                height='600',
                width='80%'
            ),
            'theme': Theme.DARK
        }
        
        config = parse_config(config_dict)
        assert isinstance(config.render.mode, RenderMode.OnLoad)
        assert config.container.direction == Directions.LEFT
        assert config.container.height == '600'
        assert config.container.width == '80%'
        assert config.theme == Theme.DARK
    
    def test_parse_legacy_config(self):
        """Test parsing legacy configuration format."""
        config_dict = {
            'render': {
                'mode': RenderMode.OnScreen(threshold=0.3, margin='100px')
            },
            'container': {
                'direction': Directions.TOP,
                'height': '700',
                'width': '95%'
            },
            'theme': Theme.LIGHT
        }
        
        config = parse_config(config_dict)
        assert isinstance(config.render.mode, RenderMode.OnScreen)
        assert config.render.mode.threshold == 0.3
        assert config.render.mode.margin == '100px'
        assert config.container.direction == Directions.TOP
        assert config.theme == Theme.LIGHT
    
    def test_parse_partial_config(self):
        """Test parsing partial configuration."""
        config_dict = {
            'theme': Theme.DARK
        }
        
        config = parse_config(config_dict)
        assert isinstance(config.render.mode, RenderMode.OnClick)
        assert config.container.direction == Directions.RIGHT
        assert config.theme == Theme.DARK


class TestGetConfigValues:
    """Test configuration value extraction."""
    
    def test_get_config_values_onclick(self):
        """Test getting configuration values for OnClick mode."""
        config = JsonCrackConfig(
            render=RenderConfig(RenderMode.OnClick()),
            container=ContainerConfig(
                direction=Directions.LEFT,
                height='400',
                width='90%'
            ),
            theme=Theme.LIGHT
        )
        
        values = get_config_values(config)
        
        assert values['render_mode'] == 'onclick'
        assert values['theme'] == 'light'
        assert values['direction'] == 'LEFT'
        assert values['height'] == '400'
        assert values['width'] == '90%'
        assert values['onscreen_threshold'] == 0.1  # default
        assert values['onscreen_margin'] == '50px'  # default
    
    def test_get_config_values_onscreen(self):
        """Test getting configuration values for OnScreen mode."""
        config = JsonCrackConfig(
            render=RenderConfig(RenderMode.OnScreen(threshold=0.5, margin='25px')),
            theme=Theme.AUTO
        )
        
        values = get_config_values(config)
        
        assert values['render_mode'] == 'onscreen'
        assert values['theme'] is None  # AUTO theme
        assert values['onscreen_threshold'] == 0.5
        assert values['onscreen_margin'] == '25px'
    
    def test_get_config_values_onload(self):
        """Test getting configuration values for OnLoad mode."""
        config = JsonCrackConfig(
            render=RenderConfig(RenderMode.OnLoad()),
            theme=Theme.DARK
        )
        
        values = get_config_values(config)
        
        assert values['render_mode'] == 'onload'
        assert values['theme'] == 'dark'
        assert values['onscreen_threshold'] == 0.1  # default
        assert values['onscreen_margin'] == '50px'  # default
    
    def test_get_config_values_default(self):
        """Test getting configuration values with default config."""
        config = JsonCrackConfig()
        values = get_config_values(config)
        
        assert values['render_mode'] == 'onclick'
        assert values['theme'] is None
        assert values['direction'] == 'RIGHT'
        assert values['height'] == '500'
        assert values['width'] == '100%'
        assert values['onscreen_threshold'] == 0.1
        assert values['onscreen_margin'] == '50px'
