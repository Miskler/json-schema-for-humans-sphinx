Configuration
=============

This page describes all available configuration options for the JSONCrack Sphinx extension.

Global Configuration
--------------------

Add these settings to your ``conf.py`` file:

Schema Directory
~~~~~~~~~~~~~~~~

.. code-block:: python

    # Path to directory containing schema files
    json_schema_dir = 'path/to/schemas'

If not specified, the extension will look for schemas in the same directory as the Python files.

Default JSONCrack Options
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from jsoncrack_for_sphinx.config import (
        RenderMode, Directions, Theme, ContainerConfig, RenderConfig,
        SearchPolicy, PathSeparator
    )

    jsoncrack_default_options = {
        'render': RenderConfig(
            mode=RenderMode.OnScreen(threshold=0.1, margin='50px')
        ),
        'container': ContainerConfig(
            direction=Directions.DOWN,
            height='500',
            width='100%'
        ),
        'theme': Theme.AUTO,
        'search_policy': SearchPolicy(
            include_package_name=False,
            path_to_file_separator=PathSeparator.DOT,
            path_to_class_separator=PathSeparator.DOT
        )
    }

Render Modes
~~~~~~~~~~~~

The extension supports different render modes:

* ``RenderMode.OnScreen(threshold, margin)`` - Renders when element comes into view
* ``RenderMode.OnClick()`` - Renders when user clicks on the element
* ``RenderMode.OnLoad()`` - Renders immediately when page loads

Container Configuration
~~~~~~~~~~~~~~~~~~~~~~~

Configure the appearance of the JSONCrack container:

* ``direction`` - Layout direction (``Directions.UP``, ``Directions.DOWN``, ``Directions.LEFT``, ``Directions.RIGHT``)
* ``height`` - Container height (e.g., ``'500'``, ``'100%'``)
* ``width`` - Container width (e.g., ``'100%'``, ``'800px'``)

Theme Options
~~~~~~~~~~~~~

* ``Theme.AUTO`` - Automatically match the documentation theme
* ``Theme.LIGHT`` - Always use light theme
* ``Theme.DARK`` - Always use dark theme

Schema Directive Options
------------------------

The ``schema`` directive supports these options:

.. code-block:: rst

    .. schema:: schema_name
       :title: Schema Title
       :description: Schema description
       :render_mode: onclick|onload|onscreen
       :direction: UP|DOWN|LEFT|RIGHT
       :height: 500
       :width: 100%
       :theme: auto|light|dark

File Naming Conventions
-----------------------

The extension looks for schema files using these naming patterns:

* ``function_name.schema.json``
* ``function_name.json``
* ``ClassName.method_name.schema.json``
* ``ClassName.method_name.json``

For example, if you have a function ``process_data``, the extension will look for:

* ``process_data.schema.json``
* ``process_data.json``

Schema Search Policy
--------------------

Configure how schema files are searched and matched to code objects using the ``SearchPolicy`` class.

Basic Search Policy
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from jsoncrack_for_sphinx.config import SearchPolicy, PathSeparator

    jsoncrack_default_options = {
        'search_policy': SearchPolicy(
            include_package_name=False,  # Include package path
            include_path_to_file=True,   # Include intermediate path components  
            path_to_file_separator=PathSeparator.DOT,  # Path separator
            path_to_class_separator=PathSeparator.DOT,  # Class separator
            custom_patterns=[]  # Additional patterns
        )
    }

Path Separators
~~~~~~~~~~~~~~~

Choose how path components are separated in filenames:

* ``PathSeparator.DOT`` - Use dots: ``MyClass.method.schema.json``
* ``PathSeparator.SLASH`` - Use slashes: ``MyClass/method.schema.json``
* ``PathSeparator.NONE`` - No separator: ``MyClassmethod.schema.json``

Path Component Control
~~~~~~~~~~~~~~~~~~~~~~

Control which parts of the object path are included in search patterns:

* ``include_package_name`` - Whether to include the root package name (e.g., ``mypackage``)
* ``include_path_to_file`` - Whether to include intermediate path components (e.g., ``module`` in ``mypackage.module.MyClass.method``)

This is useful when you want to skip intermediate namespace parts like ``endpoints.catalog`` in ``perekrestok_api.endpoints.catalog.ProductService.similar``.

Search Examples
~~~~~~~~~~~~~~~

For the object ``mypackage.module.MyClass.method``:

**Default policy (include intermediate paths, dot separators):**

.. code-block:: text

    MyClass.method.schema.json              # Highest priority
    module.MyClass.method.schema.json       # Intermediate path included
    method.schema.json
    mypackage.module.MyClass.method.schema.json

**Skip intermediate paths:**

.. code-block:: python

    SearchPolicy(
        include_path_to_file=False
    )

.. code-block:: text

    MyClass.method.schema.json              # Highest priority
    method.schema.json                      # Skip "module.MyClass.method"
    mypackage.module.MyClass.method.schema.json

**With package names and slash separators:**

.. code-block:: python

    SearchPolicy(
        include_package_name=True,
        include_path_to_file=True,
        path_to_file_separator=PathSeparator.SLASH
    )

.. code-block:: text

    MyClass.method.schema.json
    mypackage/module/MyClass.method.schema.json
    module/MyClass.method.schema.json
    method.schema.json

Custom Patterns
~~~~~~~~~~~~~~~

Add custom search patterns using placeholders:

.. code-block:: python

    SearchPolicy(
        custom_patterns=[
            'api_{class_name}_{method_name}.json',
            '{object_name}_specification.json',
            'custom_{method_name}.schema.json'
        ]
    )

Available placeholders:

* ``{object_name}`` - Full object name (e.g., ``mypackage.module.MyClass.method``)
* ``{class_name}`` - Class name only (e.g., ``MyClass``)
* ``{method_name}`` - Method/function name only (e.g., ``method``)
* ``{package_name}`` - Package path (e.g., ``mypackage.module``)

Debug Logging
~~~~~~~~~~~~~

Enable debug logging to troubleshoot schema detection:

.. code-block:: python

    # In conf.py
    jsoncrack_debug_logging = True

This outputs detailed information about:

* Which patterns are generated and tried
* Why certain patterns match or don't match
* File system search results
* Final schema resolution

Real-World Example
~~~~~~~~~~~~~~~~~

For a complex API like ``perekrestok_api.endpoints.catalog.ProductService.similar``:

.. code-block:: python

    # This configuration would find ProductService.similar.schema.json
    SearchPolicy(
        include_package_name=False,  # Ignore package path
        path_to_file_separator=PathSeparator.DOT,
        path_to_class_separator=PathSeparator.DOT
    )

    # This would also look for perekrestok_api/endpoints/catalog/ProductService.similar.schema.json
    SearchPolicy(
        include_package_name=True,
        path_to_file_separator=PathSeparator.SLASH,
        path_to_class_separator=PathSeparator.DOT
    )

Advanced Configuration
----------------------

Custom Schema Resolvers
~~~~~~~~~~~~~~~~~~~~~~~~

You can provide custom logic for finding schema files:

.. code-block:: python

    def custom_schema_resolver(obj_name, obj_type):
        """Custom function to resolve schema file paths."""
        if obj_type == 'function':
            return f'schemas/{obj_name}.custom.json'
        return None

    jsoncrack_schema_resolver = custom_schema_resolver

Error Handling
~~~~~~~~~~~~~~

Configure how the extension handles missing or invalid schemas:

.. code-block:: python

    # Skip missing schemas silently (default: False)
    jsoncrack_ignore_missing = True
    
    # Log warnings for invalid schemas (default: True)
    jsoncrack_log_warnings = True
