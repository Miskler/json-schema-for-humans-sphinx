Examples
========

This section provides practical examples of using the JSONCrack Sphinx extension.

Automatic Schema Documentation
------------------------------

This example demonstrates how schemas are automatically included when using autodoc.

.. automodule:: example_module
   :members:
   :undoc-members:
   :show-inheritance:

Manual Schema Inclusion
-----------------------

The following examples show how to manually include schemas using the ``schema`` directive.

User Creation Schema
~~~~~~~~~~~~~~~~~~~~

.. schema:: User.create
   :title: User Creation Schema
   :description: Schema for creating new users
   :render_mode: onclick
   :direction: RIGHT
   :height: 500

Data Processing Schema with Auto-load
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. schema:: process_data
   :title: Data Processing Schema
   :description: Schema for processing data
   :render_mode: onload
   :direction: DOWN
   :height: 600

User Update Schema with Different Direction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. schema:: User.update
   :title: User Update Schema 
   :description: Schema for updating existing users
   :render_mode: onclick
   :direction: LEFT
   :height: 450

Complex Schema with OnScreen Rendering
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. schema:: User.example
   :title: User Example Schema
   :description: Complex example schema with detailed structure
   :render_mode: onscreen
   :direction: DOWN
   :height: 700
   :width: 95%

Schema Files
------------

The examples use the following schema files located in the ``examples/schemas/`` directory:

* ``User.create.schema.json`` - Schema for user creation
* ``User.update.schema.json`` - Schema for user updates  
* ``User.example.json`` - Example user data structure
* ``process_data.schema.json`` - Schema for data processing
* ``ProductService.similar.schema.json`` - Example for complex naming patterns

These schemas demonstrate various JSON Schema features including:

- Object definitions with required and optional properties
- Array handling with item schemas
- String pattern validation
- Numeric constraints
- Nested object structures
- Conditional schema validation

Advanced Search Policy Examples
-------------------------------

Complex Object Names
~~~~~~~~~~~~~~~~~~~~

This example shows how the new search policy handles complex object names like ``perekrestok_api.endpoints.catalog.ProductService.similar``.

With the default search policy, the extension automatically finds ``ProductService.similar.schema.json``:

.. schema:: ProductService.similar
   :title: Product Service Similar Items
   :description: Schema for finding similar products in the catalog
   :render_mode: onclick

Custom Search Patterns
~~~~~~~~~~~~~~~~~~~~~~

You can configure custom search patterns in your ``conf.py``:

.. code-block:: python

    from jsoncrack_for_sphinx.config import SearchPolicy, PathSeparator

    jsoncrack_default_options = {
        'search_policy': SearchPolicy(
            include_package_name=True,
            path_to_file_separator=PathSeparator.SLASH,
            custom_patterns=[
                'api_{class_name}_{method_name}.json',
                '{object_name}_spec.json'
            ]
        )
    }

This configuration would search for schemas in this order:

1. ``ProductService.similar.schema.json`` (highest priority)
2. ``api_ProductService_similar.json`` (custom pattern)
3. ``perekrestok_api.endpoints.catalog.ProductService.similar_spec.json`` (custom pattern)
4. ``perekrestok_api/endpoints/catalog/ProductService.similar.schema.json`` (with package path)
5. ``catalog/ProductService.similar.schema.json`` (parent module)
6. ``similar.schema.json`` (method name only)

Debug Output Example
~~~~~~~~~~~~~~~~~~~

When ``jsoncrack_debug_logging = True`` is enabled, you'll see output like:

.. code-block:: text

    DEBUG: Searching for schema for object: perekrestok_api.endpoints.catalog.ProductService.similar
    DEBUG: Generated search patterns:
    DEBUG:   1. ProductService.similar.schema.json (priority: 100)
    DEBUG:   2. catalog.ProductService.similar.schema.json (priority: 80)
    DEBUG:   3. similar.schema.json (priority: 60)
    DEBUG:   4. perekrestok_api.endpoints.catalog.ProductService.similar.schema.json (priority: 40)
    DEBUG: Checking file: /path/to/schemas/ProductService.similar.schema.json
    DEBUG: ✓ Found schema file: ProductService.similar.schema.json
