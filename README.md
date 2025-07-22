# JSONCrack for Sphinx Extension

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/jsoncrack-for-sphinx)
[![PyPI - Package Version](https://img.shields.io/pypi/v/jsoncrack-for-sphinx?color=blue)](https://pypi.org/project/jsoncrack-for-sphinx/)
[![Coverage](https://miskler.github.io/jsoncrack-for-sphinx/coverage.svg)](https://miskler.github.io/jsoncrack-for-sphinx/coverage/)
[![Test Summary](https://miskler.github.io/jsoncrack-for-sphinx/tests-badge.svg)](https://miskler.github.io/jsoncrack-for-sphinx/tests/test-report.html)
[![Discord](https://img.shields.io/discord/792572437292253224?label=Discord&labelColor=%232c2f33&color=%237289da)](https://discord.gg/UnJnGHNbBp)
[![Telegram](https://img.shields.io/badge/Telegram-24A1DE)](https://t.me/miskler_dev)

📖 **[Documentation](https://miskler.github.io/jsoncrack-for-sphinx/quickstart)** | 📊 **[Coverage Report](https://miskler.github.io/jsoncrack-for-sphinx/coverage/)** | 🔬 **[Examples](https://miskler.github.io/jsoncrack-for-sphinx/examples)**

This package provides a Sphinx extension that automatically adds JSON schemas to function and method documentation. It uses [jsoncrack.com](https://jsoncrack.com/) to generate beautiful, interactive HTML representations of JSON schemas.

## Features

- 🔄 **Automatic schema inclusion**: Schemas are automatically included in autodoc-generated documentation
- 📁 **Flexible file naming**: Support for multiple naming conventions
- 🎨 **Beautiful rendering**: Uses JSONCrack for rich interactive visualization
- 🔧 **Manual inclusion**: `schema` directive for manual schema inclusion
- 🧪 **Testing support**: Fixtures for testing schema documentation
- 🌙 **Dark mode**: Support for dark theme styling
- 📊 **Multiple render modes**: `onclick`, `onload`, and `onscreen` loading modes
- 🔍 **JSON && Schema**: Supports both JSON schemas (.schema.json) and plain JSON files (.json)

## Installation

```bash
pip install jsoncrack-for-sphinx
```

## Quick Start

### 1. Configure Sphinx

Add the extension to your `conf.py`:

```python
extensions = [
    "sphinx.ext.autodoc",
    "jsoncrack_for_sphinx",
]

# Configure schema directory
json_schema_dir = os.path.join(os.path.dirname(__file__), "schemas")
```

### 2. Create Schema Files

Create schema files following the naming convention:

```
schemas/
├── MyClass.my_method.schema.json        # Method schema
├── MyClass.my_method.options.schema.json # Method with options
├── my_function.schema.json              # Function schema
└── my_function.advanced.schema.json     # Function with options
```

### 3. Document Your Code

```python
class MyClass:
    def my_method(self, data):
        """
        Process data according to schema.
        
        Args:
            data: Input data (schema automatically included)
        """
        pass
```

The schema will be automatically included in the generated documentation!

## File Naming Convention

The extension searches for schema files using these patterns:

- `<ClassName>.<method>.<option-name>.schema.json`
- `<ClassName>.<method>.schema.json`
- `<function>.<option-name>.schema.json`
- `<function>.schema.json`

**Note**: If a function belongs to a class, the class name must be included in the filename.

## Schema Search Policies

The extension provides powerful and flexible schema file search capabilities through configurable search policies:

### Quick Examples

For object `perekrestok_api.endpoints.catalog.ProductService.similar`:

**Default (include intermediate paths):**
```
ProductService.similar.schema.json          # Highest priority
catalog.ProductService.similar.schema.json  
endpoints.catalog.ProductService.similar.schema.json
similar.schema.json
```

**Skip intermediate paths (cleaner naming):**
```python
SearchPolicy(include_path_to_file=False)
```
```
ProductService.similar.schema.json          # Only class+method
similar.schema.json                          # Method only
# Skips: "catalog.ProductService.similar.schema.json"
```

**Directory-based organization:**
```python
SearchPolicy(path_to_file_separator=PathSeparator.SLASH)
```
```
ProductService.similar.schema.json
endpoints/catalog/ProductService.similar.schema.json  # Uses directories
similar.schema.json
```

**Custom API patterns:**
```python
SearchPolicy(custom_patterns=['api_{class_name}_{method_name}.json'])
```
```
api_ProductService_similar.json             # Custom pattern
ProductService.similar.schema.json          # Standard patterns
```

📖 **[Complete Search Patterns Guide](https://miskler.github.io/jsoncrack-for-sphinx/search_patterns.html)** - Detailed analysis of all 8 combinations with examples

## Advanced Schema Search Configuration

### Configurable Search Policy

The extension supports flexible schema file naming conventions through the `SearchPolicy` configuration. See the [Complete Search Patterns Guide](https://miskler.github.io/jsoncrack-for-sphinx/search_patterns.html) for detailed examples and all possible configurations.

## Manual Schema Inclusion

You can also manually include schemas using the `schema` directive:

```rst
.. schema:: MyClass.my_method
   :title: Custom Title
   :description: Custom description
   :render_mode: onclick
   :direction: RIGHT
   :height: 500
```

## Configuration Options

Configure the extension in your `conf.py`:

### New Structured Configuration (Recommended)

```python
from jsoncrack_for_sphinx.config import (
    RenderMode, Directions, Theme, ContainerConfig, RenderConfig,
    SearchPolicy, PathSeparator
)

# Required: Directory containing schema files
json_schema_dir = "path/to/schemas"

# JSONCrack configuration
jsoncrack_default_options = {
    'render': RenderConfig(
        mode=RenderMode.OnClick()  # or OnLoad(), OnScreen(threshold=0.1, margin='50px')
    ),
    'container': ContainerConfig(
        direction=Directions.RIGHT,  # TOP, RIGHT, DOWN, LEFT
        height='500',  # Height in pixels
        width='100%'   # Width in pixels or percentage
    ),
    'theme': Theme.AUTO,  # AUTO, LIGHT, DARK
    'search_policy': SearchPolicy(
        include_package_name=False,  # Include package path in search patterns
        path_to_file_separator=PathSeparator.DOT,  # How to separate path components
        path_to_class_separator=PathSeparator.DOT,  # How to separate class/method
        custom_patterns=['custom_{class_name}_{method_name}.json']  # Additional patterns
    ),
    'disable_autodoc': False,  # Disable automatic schema detection
    'autodoc_ignore': []  # List of paths to ignore in autodoc (uses "starts with" logic)
}
```

### Legacy Configuration (Still Supported)

```python
# Required: Directory containing schema files
json_schema_dir = "path/to/schemas"

# JSONCrack configuration
jsoncrack_render_mode = 'onclick'  # 'onclick', 'onload', or 'onscreen'
jsoncrack_theme = None  # 'light', 'dark' or None (auto-detect from page)
jsoncrack_direction = 'RIGHT'  # 'TOP', 'RIGHT', 'DOWN', 'LEFT'
jsoncrack_height = '500'  # Height in pixels
jsoncrack_width = '100%'  # Width in pixels or percentage

# Onscreen mode configuration
jsoncrack_onscreen_threshold = 0.1  # Visibility threshold (0.0-1.0)
jsoncrack_onscreen_margin = '50px'  # Root margin for early loading

# Autodoc control
jsoncrack_disable_autodoc = False  # Disable automatic schema detection
jsoncrack_autodoc_ignore = []  # List of paths to ignore in autodoc
```

### Render Modes

- **`RenderMode.OnClick()`**: Schema loads when user clicks the button (default)
- **`RenderMode.OnLoad()`**: Schema loads immediately when page loads
- **`RenderMode.OnScreen(threshold=0.1, margin='50px')`**: Schema loads automatically when visible

### Render Mode Parameters

- **`threshold`**: Percentage of element that must be visible (0.0-1.0)
- **`margin`**: Distance before element enters viewport to start loading

### Container Configuration

- **`direction`**: Visualization direction (`Directions.TOP`, `RIGHT`, `DOWN`, `LEFT`)
- **`height`**: Container height in pixels (string or int)
- **`width`**: Container width in pixels or percentage (string or int)

### Theme Options

- **`Theme.AUTO`**: Auto-detect from page (default)
- **`Theme.LIGHT`**: Force light theme
- **`Theme.DARK`**: Force dark theme

### File Types

- **`.schema.json`**: JSON Schema files - generates fake data using JSF
- **`.json`**: Plain JSON files - renders the JSON data as-is

## Testing Support

The extension provides fixtures for testing:

```python
from jsoncrack_for_sphinx.fixtures import schema_to_rst_fixture

def test_schema_documentation(schema_to_rst_fixture):
    rst_content = schema_to_rst_fixture(schema_path, title="Test Schema")
    assert "Test Schema" in rst_content
```

## Development

### Setup

```bash
git clone https://github.com/miskler/jsoncrack-for-sphinx.git
cd jsoncrack-for-sphinx
make install-dev
```

### Commands

```bash
make test        # Run tests
make lint        # Run linting
make format      # Format code
make type-check  # Run type checking
make build       # Build package
make example-docs # Build example documentation
```

### Example

See the `examples/` directory for a complete working example:

```bash
cd examples/docs
sphinx-build -b html . _build/html
```

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
