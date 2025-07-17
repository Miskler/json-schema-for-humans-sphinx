# JSONCrack for Sphinx Extension

[![CI](https://github.com/yourusername/json-schema-for-humans-sphinx/actions/workflows/ci.yml/badge.svg)](https://github.com/yourusername/json-schema-for-humans-sphinx/actions/workflows/ci.yml)
[![PyPI version](https://badge.fury.io/py/stoplightio-schema-sphinx.svg)](https://badge.fury.io/py/stoplightio-schema-sphinx)
[![Python versions](https://img.shields.io/pypi/pyversions/stoplightio-schema-sphinx.svg)](https://pypi.org/project/stoplightio-schema-sphinx/)

This package provides a Sphinx extension that automatically adds JSON schemas to function and method documentation. It uses [json-schema-for-humans](https://github.com/coveooss/json-schema-for-humans) to generate beautiful, interactive HTML representations of JSON schemas.

## Features

- 🔄 **Automatic schema inclusion**: Schemas are automatically included in autodoc-generated documentation
- 📁 **Flexible file naming**: Support for multiple naming conventions
- 🎨 **Beautiful rendering**: Uses json-schema-for-humans for rich HTML output
- 🔧 **Manual inclusion**: `schema` directive for manual schema inclusion
- 🧪 **Testing support**: Fixtures for testing schema documentation
- 🌙 **Dark mode**: Support for dark theme styling

## Installation

```bash
pip install stoplightio-schema-sphinx
```

## Quick Start

### 1. Configure Sphinx

Add the extension to your `conf.py`:

```python
extensions = [
    "sphinx.ext.autodoc",
    "stoplightio_schema_sphinx",
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

## Manual Schema Inclusion

You can also manually include schemas using the `schema` directive:

```rst
.. schema:: MyClass.my_method
   :title: Custom Title
   :description: Custom description
```

## Configuration Options

Configure the extension in your `conf.py`:

```python
# Required: Directory containing schema files
json_schema_dir = "path/to/schemas"

# Optional: json-schema-for-humans configuration
json_schema_config = {
    "minify": True,
    "deprecated_from_description": True,
    "default_from_description": True,
    "expand_buttons": True,
    "template_name": "js"
}
```

## Testing Support

The extension provides fixtures for testing:

```python
from stoplightio_schema_sphinx.fixtures import schema_to_rst_fixture

def test_schema_documentation(schema_to_rst_fixture):
    rst_content = schema_to_rst_fixture(schema_path, title="Test Schema")
    assert "Test Schema" in rst_content
```

## Development

### Setup

```bash
git clone https://github.com/yourusername/json-schema-for-humans-sphinx.git
cd json-schema-for-humans-sphinx
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
