"""
Pytest configuration and fixtures for the jsoncrack-for-sphinx extension.

This module imports all fixtures from submodules for global test use.
"""

import sys
from pathlib import Path

from .fixtures_global.basic_fixtures import (
    create_test_json_file,
    create_test_schema_file,
    temp_dir,
)
from .fixtures_global.data_fixtures import sample_json_data, sample_schema
from .fixtures_global.file_fixtures import json_file, schema_dir, schema_file
from .fixtures_global.sphinx_fixtures import (
    mock_directive_args,
    mock_sphinx_app,
    mock_sphinx_env,
)
from .fixtures_global.utility_fixtures import schema_to_rst_fixture

# Add tests directory to path for absolute imports
test_dir = Path(__file__).parent
if str(test_dir) not in sys.path:
    sys.path.insert(0, str(test_dir))

# Expose all fixtures for pytest discovery
__all__ = [
    "temp_dir",
    "create_test_schema_file",
    "create_test_json_file",
    "sample_schema",
    "sample_json_data",
    "schema_file",
    "json_file",
    "schema_dir",
    "mock_sphinx_app",
    "mock_sphinx_env",
    "mock_directive_args",
    "schema_to_rst_fixture",
]
