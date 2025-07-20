Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_,
and this project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

[Unreleased]
------------

Added
~~~~~

- **🔍 Configurable Search Policy**: New ``SearchPolicy`` class for flexible schema file naming conventions
- **📁 Path Separators**: Support for dot, slash, or no separators in file names (``PathSeparator`` enum)
- **🎯 Custom Search Patterns**: Define custom patterns with placeholders like ``{class_name}`` and ``{method_name}``
- **📦 Package Path Support**: Option to include or exclude package paths in schema searches
- **🐛 Debug Logging**: Comprehensive logging for troubleshooting schema detection (``jsoncrack_debug_logging``)
- **🧪 Enhanced Testing**: Complete test suite for new search functionality
- Enhanced documentation with Furo theme
- Comprehensive usage examples
- Performance optimizations
- Better error handling

Changed
~~~~~~~

- **⚡ Improved Schema Discovery**: Completely rewritten schema search algorithm with priority-based pattern matching
- **🔧 Backward Compatibility**: Maintained full compatibility with existing configurations and file naming
- **📖 Enhanced Documentation**: Added comprehensive examples and troubleshooting guides
- Updated configuration options
- Enhanced test coverage

Fixed
~~~~~

- **🐛 Mock Object Handling**: Fixed ``TypeError`` when processing Mock objects in tests
- **🎯 Complex Object Names**: Now correctly handles deep package paths like ``perekrestok_api.endpoints.catalog.ProductService.similar``
- Fixed duplicate files cleanup
- Resolved configuration enum issues
- Fixed documentation build process

[0.1.0] - 2025-07-18
--------------------

Added
~~~~~

- Initial release of JSONCrack Sphinx extension
- Automatic schema inclusion with autodoc
- Manual schema inclusion via ``schema`` directive
- Support for multiple render modes (OnScreen, OnClick, OnLoad)
- Configurable container layouts and themes
- JSONCrack visualization integration
- Comprehensive test suite with 153 tests
- Documentation with examples
- Support for multiple schema file naming conventions
- Dark mode theme support
- Performance optimizations for large schemas

Features
~~~~~~~~

- **Automatic Schema Detection**: Automatically finds and includes schemas for documented functions and classes
- **Manual Schema Inclusion**: ``schema`` directive for manual schema inclusion with full control
- **Flexible Rendering**: OnScreen, OnClick, and OnLoad rendering modes
- **Theme Integration**: Automatic theme detection and manual theme override
- **Layout Control**: Configurable direction, height, and width options
- **Performance Optimized**: Lazy loading and efficient rendering
- **Test Coverage**: 90% test coverage with comprehensive test suite
- **Documentation**: Complete documentation with examples and API reference

Configuration
~~~~~~~~~~~~~

- ``json_schema_dir`` - Configure schema file directory
- ``jsoncrack_default_options`` - Set default rendering options
- ``RenderMode`` - Control when schemas are rendered
- ``Directions`` - Configure layout direction
- ``Theme`` - Control theme selection
- ``ContainerConfig`` - Configure container appearance
- ``RenderConfig`` - Configure rendering behavior

File Naming Conventions
~~~~~~~~~~~~~~~~~~~~~~~

- ``function_name.schema.json``
- ``function_name.json``
- ``ClassName.method_name.schema.json``
- ``ClassName.method_name.json``

Technical Details
~~~~~~~~~~~~~~~~~

- Built with Sphinx extension framework
- Uses JSONCrack for schema visualization
- Supports Python 3.8+
- Compatible with major Sphinx themes
- Comprehensive error handling
- Memory efficient implementation

Known Issues
~~~~~~~~~~~~

- None at this time

Migration Guide
~~~~~~~~~~~~~~~

This is the initial release, so no migration is needed.
