Quick Start Guide
=================

This guide will help you quickly set up and start using the JSONCrack Sphinx extension.

Installation
------------

Install the extension using pip:

.. code-block:: bash

    pip install jsoncrack-for-sphinx

Configuration
-------------

Add the extension to your Sphinx configuration file (`conf.py`):

.. code-block:: python

    extensions = [
        'jsoncrack_for_sphinx',
        # ... other extensions
    ]

    # Configure schema directory (optional)
    json_schema_dir = 'path/to/your/schemas'

    # Configure default JSONCrack options
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

Basic Usage
-----------

Manual Schema Inclusion
~~~~~~~~~~~~~~~~~~~~~~~~

Use the ``schema`` directive to include schemas manually:

.. code-block:: rst

    .. schema:: user_schema
       :title: User Schema
       :description: Schema for user data
       :render_mode: onclick
       :direction: RIGHT
       :height: 500

Automatic Schema Inclusion
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The extension automatically detects and includes schemas when using autodoc:

.. code-block:: rst

    .. automodule:: my_module
       :members:
       :undoc-members:
       :show-inheritance:

If your module contains functions with schema files, they will be automatically included in the documentation.

Next Steps
----------

- Read the :doc:`configuration` guide for advanced configuration options
- Check out the :doc:`examples` to see the extension in action
- Explore the :doc:`api` for detailed API documentation
