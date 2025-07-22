"""
Sphinx-related mock fixtures for testing.
"""

from unittest.mock import Mock

import pytest


@pytest.fixture
def mock_sphinx_app():
    """Create a mock Sphinx application for testing."""
    app = Mock()
    app.config = Mock()
    app.env = Mock()
    app.env.config = app.config

    # Default config values
    app.config.json_schema_dir = None
    app.config.jsoncrack_render_mode = "onclick"
    app.config.jsoncrack_theme = None
    app.config.jsoncrack_direction = "RIGHT"
    app.config.jsoncrack_height = "500"
    app.config.jsoncrack_width = "100%"
    app.config.jsoncrack_onscreen_threshold = 0.1
    app.config.jsoncrack_onscreen_margin = "50px"
    app.config.html_static_path = []

    # Mock methods
    app.add_config_value = Mock()
    app.add_directive = Mock()
    app.connect = Mock()
    app.add_css_file = Mock()
    app.add_js_file = Mock()

    return app


@pytest.fixture
def mock_sphinx_env():
    """Create a mock Sphinx environment for testing."""
    env = Mock()
    env.config = Mock()
    env.config.json_schema_dir = None
    return env


@pytest.fixture
def mock_directive_args():
    """Create mock arguments for directive testing."""
    return {
        "arguments": ["User.create"],
        "options": {
            "title": "Test Schema",
            "description": "Test description",
            "render_mode": "onclick",
            "direction": "RIGHT",
            "height": "500",
        },
        "content": [],
        "content_offset": 0,
        "block_text": "",
        "state": Mock(),
        "state_machine": Mock(),
    }
