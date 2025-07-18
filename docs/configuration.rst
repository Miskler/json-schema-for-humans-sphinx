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

    from jsoncrack_for_sphinx import RenderMode, Directions, Theme, ContainerConfig, RenderConfig

    jsoncrack_default_options = {
        'render': RenderConfig(
            mode=RenderMode.OnScreen(threshold=0.1, margin='50px')
        ),
        'container': ContainerConfig(
            direction=Directions.DOWN,
            height='500',
            width='100%'
        ),
        'theme': Theme.AUTO
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
