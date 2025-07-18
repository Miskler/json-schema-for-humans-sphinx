Development Guide
=================

This guide covers how to set up a development environment and contribute to the JSONCrack Sphinx extension.

Setting Up Development Environment
----------------------------------

Prerequisites
~~~~~~~~~~~~~

- Python 3.8 or higher
- Git
- Virtual environment tool (venv, conda, etc.)

Installation
~~~~~~~~~~~~

1. Clone the repository:

.. code-block:: bash

    git clone https://github.com/miskler/json-schema-for-humans-sphinx.git
    cd json-schema-for-humans-sphinx

2. Create and activate a virtual environment:

.. code-block:: bash

    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install development dependencies:

.. code-block:: bash

    pip install -r requirements-dev.txt
    pip install -e .

Running Tests
-------------

The project uses pytest for testing. Run the complete test suite:

.. code-block:: bash

    pytest

Run with coverage:

.. code-block:: bash

    pytest --cov=jsoncrack_for_sphinx --cov-report=html

Run specific test files:

.. code-block:: bash

    pytest tests/test_extension.py
    pytest tests/test_config.py

Building Documentation
----------------------

Build the main documentation:

.. code-block:: bash

    cd docs
    make html

Build the examples documentation:

.. code-block:: bash

    cd examples/docs
    make html

Serve documentation locally:

.. code-block:: bash

    # From project root
    ./serve-docs.sh

Project Structure
-----------------

.. code-block:: text

    json-schema-for-humans-sphinx/
    ├── src/jsoncrack_for_sphinx/     # Main extension code
    │   ├── __init__.py              # Package initialization
    │   ├── extension.py             # Main Sphinx extension
    │   ├── config.py                # Configuration classes
    │   ├── utils.py                 # Utility functions
    │   ├── fixtures.py              # Test fixtures
    │   └── static/                  # Static assets
    ├── tests/                       # Test suite
    ├── docs/                        # Main documentation
    ├── examples/                    # Usage examples
    │   ├── example_module.py        # Example Python module
    │   ├── schemas/                 # Example schemas
    │   └── docs/                    # Example documentation
    └── requirements-dev.txt         # Development dependencies

Code Style
----------

The project follows PEP 8 style guidelines. Use these tools:

.. code-block:: bash

    # Format code
    black src/ tests/
    
    # Check style
    flake8 src/ tests/
    
    # Sort imports
    isort src/ tests/

Testing Guidelines
------------------

Write Tests
~~~~~~~~~~~

- Write tests for all new functionality
- Maintain high test coverage (>90%)
- Use descriptive test names
- Include both positive and negative test cases

Test Organization
~~~~~~~~~~~~~~~~~

- ``test_extension.py`` - Core extension functionality
- ``test_config.py`` - Configuration classes
- ``test_utils.py`` - Utility functions
- ``test_fixtures.py`` - Test fixtures
- ``test_integration.py`` - Integration tests
- ``test_performance.py`` - Performance tests

Mock External Dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~

Use mocks for external dependencies:

.. code-block:: python

    from unittest.mock import Mock, patch
    
    @patch('jsoncrack_for_sphinx.utils.read_schema_file')
    def test_schema_loading(mock_read):
        mock_read.return_value = {"type": "object"}
        # Test implementation

Contributing
------------

Pull Request Process
~~~~~~~~~~~~~~~~~~~~

1. Fork the repository
2. Create a feature branch: ``git checkout -b feature/my-feature``
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Update documentation if needed
7. Commit your changes: ``git commit -m "Add my feature"``
8. Push to your fork: ``git push origin feature/my-feature``
9. Create a pull request

Code Review
~~~~~~~~~~~

All pull requests require code review. Please:

- Write clear commit messages
- Keep changes focused and atomic
- Include tests for new features
- Update documentation as needed
- Respond to feedback promptly

Release Process
---------------

1. Update version in ``pyproject.toml``
2. Update ``CHANGELOG.md``
3. Create a git tag: ``git tag v0.1.0``
4. Push tag: ``git push origin v0.1.0``
5. Build and publish to PyPI:

.. code-block:: bash

    python -m build
    twine upload dist/*

Debugging
---------

Enable debug logging:

.. code-block:: python

    import logging
    logging.basicConfig(level=logging.DEBUG)

Use the Sphinx verbose mode:

.. code-block:: bash

    sphinx-build -v -W docs _build/html

Common Issues
~~~~~~~~~~~~~

**Schema not found**: Check file paths and naming conventions
**Import errors**: Ensure the package is installed in development mode
**Test failures**: Run tests individually to isolate issues
