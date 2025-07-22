"""
Integration tests for configuration and file handling.
"""

import json
from pathlib import Path
from unittest.mock import Mock

from jsoncrack_for_sphinx.config import (
    ContainerConfig,
    Directions,
    RenderConfig,
    RenderMode,
    Theme,
)
from jsoncrack_for_sphinx.config.config_utils import get_jsoncrack_config
from jsoncrack_for_sphinx.schema.schema_finder import find_schema_for_object


class TestConfigIntegration:
    """Integration tests for configuration handling."""

    def test_config_integration(self, temp_dir):
        """Test configuration integration with different settings."""
        # Test new-style configuration
        mock_config = Mock()
        mock_config.jsoncrack_default_options = {
            "render": RenderConfig(RenderMode.OnScreen(threshold=0.2, margin="75px")),
            "container": ContainerConfig(
                direction=Directions.LEFT, height="600", width="95%"
            ),
            "theme": Theme.DARK,
        }

        config = get_jsoncrack_config(mock_config)

        assert isinstance(config.render.mode, RenderMode.OnScreen)
        assert config.render.mode.threshold == 0.2
        assert config.render.mode.margin == "75px"
        assert config.container.direction == Directions.LEFT
        assert config.container.height == "600"
        assert config.container.width == "95%"
        assert config.theme == Theme.DARK

        # Test legacy configuration
        mock_config_legacy = Mock()
        (
            delattr(mock_config_legacy, "jsoncrack_default_options")
            if hasattr(mock_config_legacy, "jsoncrack_default_options")
            else None
        )

        mock_config_legacy.jsoncrack_render_mode = "onload"
        mock_config_legacy.jsoncrack_direction = "TOP"
        mock_config_legacy.jsoncrack_theme = "light"
        mock_config_legacy.jsoncrack_height = "400"
        mock_config_legacy.jsoncrack_width = "80%"
        mock_config_legacy.jsoncrack_onscreen_threshold = 0.3
        mock_config_legacy.jsoncrack_onscreen_margin = "100px"

        config_legacy = get_jsoncrack_config(mock_config_legacy)

        assert isinstance(config_legacy.render.mode, RenderMode.OnLoad)
        assert config_legacy.container.direction == Directions.TOP
        assert config_legacy.container.height == "400"
        assert config_legacy.container.width == "80%"
        assert config_legacy.theme == Theme.LIGHT

    def test_schema_file_types_integration(self, temp_dir):
        """Test integration with different schema file types."""
        schema_dir = temp_dir / "schemas"
        schema_dir.mkdir()

        # Create .schema.json file
        schema_data = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "title": "Test Schema",
            "properties": {"name": {"type": "string"}},
        }

        with open(schema_dir / "test.schema.json", "w") as f:
            json.dump(schema_data, f)

        # Create .json file
        json_data = {"name": "Test User", "email": "test@example.com", "age": 30}

        with open(schema_dir / "example.json", "w") as f:
            json.dump(json_data, f)

        # Test finding schema file
        schema_result = find_schema_for_object("module.test", str(schema_dir))
        assert schema_result is not None
        schema_path, file_type = schema_result
        assert Path(schema_path).name == "test.schema.json"
        assert file_type == "schema"

        # Test finding JSON file
        json_result = find_schema_for_object("module.example", str(schema_dir))
        assert json_result is not None
        json_path, file_type = json_result
        assert Path(json_path).name == "example.json"
        assert file_type == "json"
