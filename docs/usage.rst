Usage Guide
===========

This guide covers the different ways to use the JSONCrack Sphinx extension in your documentation.

Automatic Schema Inclusion
---------------------------

The extension automatically detects and includes schemas when using Sphinx's autodoc functionality.

Setup
~~~~~

1. Ensure your schema files are in the correct location (same directory as Python files or in the configured ``json_schema_dir``)
2. Use standard autodoc directives in your RST files

Example Python module (``my_module.py``):

.. code-block:: python

    def process_data(data):
        """Process user data according to schema.
        
        This function processes data according to the schema
        defined in process_data.schema.json.
        """
        # Function implementation
        pass

    class User:
        def create(self, user_data):
            """Create a new user.
            
            Schema: User.create.schema.json
            """
            pass

RST documentation:

.. code-block:: rst

    .. automodule:: my_module
       :members:
       :undoc-members:
       :show-inheritance:

The extension will automatically find and include:
- ``process_data.schema.json`` for the ``process_data`` function
- ``User.create.schema.json`` for the ``User.create`` method

Manual Schema Inclusion
------------------------

Use the ``schema`` directive to manually include schemas with full control over presentation.

Basic Usage
~~~~~~~~~~~

.. code-block:: rst

    .. schema:: user_schema
       :title: User Schema
       :description: Schema for user data validation

Advanced Options
~~~~~~~~~~~~~~~~

.. code-block:: rst

    .. schema:: complex_schema
       :title: Complex Data Schema
       :description: Schema for complex data structures
       :render_mode: onclick
       :direction: RIGHT
       :height: 600
       :width: 90%
       :theme: dark

Render Modes
~~~~~~~~~~~~

**OnScreen Rendering** (default):

.. code-block:: rst

    .. schema:: schema_name
       :render_mode: onscreen

Renders when the element comes into view. Best for performance with many schemas.

**OnClick Rendering**:

.. code-block:: rst

    .. schema:: schema_name
       :render_mode: onclick

Renders when user clicks on the element. Good for large schemas that might slow down page loading.

**OnLoad Rendering**:

.. code-block:: rst

    .. schema:: schema_name
       :render_mode: onload

Renders immediately when the page loads. Use sparingly as it can impact page performance.

Layout Options
--------------

Direction
~~~~~~~~~

Control the flow direction of the schema visualization:

.. code-block:: rst

    .. schema:: schema_name
       :direction: UP      # Elements flow upward
       :direction: DOWN    # Elements flow downward (default)
       :direction: LEFT    # Elements flow leftward
       :direction: RIGHT   # Elements flow rightward

Size Configuration
~~~~~~~~~~~~~~~~~~

.. code-block:: rst

    .. schema:: schema_name
       :height: 500        # Fixed height in pixels
       :height: 100%       # Percentage of container
       :width: 800         # Fixed width in pixels  
       :width: 100%        # Full width (default)

Theme Integration
-----------------

The extension integrates with your documentation theme:

.. code-block:: rst

    .. schema:: schema_name
       :theme: auto        # Match documentation theme (default)
       :theme: light       # Always use light theme
       :theme: dark        # Always use dark theme

Working with Multiple Schemas
------------------------------

You can include multiple schemas in a single document:

.. code-block:: rst

    User Management Schemas
    =======================

    User Creation
    -------------

    .. schema:: User.create
       :title: User Creation Schema
       :description: Schema for creating new users
       :render_mode: onclick

    User Update
    -----------

    .. schema:: User.update
       :title: User Update Schema  
       :description: Schema for updating existing users
       :render_mode: onclick

    Data Processing
    ---------------

    .. schema:: process_data
       :title: Data Processing Schema
       :description: Schema for processing user data
       :render_mode: onscreen

Best Practices
--------------

1. **Use descriptive titles and descriptions** for better user experience
2. **Choose appropriate render modes** based on schema complexity and page performance
3. **Organize schemas logically** using proper headings and sections
4. **Test different layout directions** to find the best fit for your content
5. **Consider mobile users** when setting container dimensions

Troubleshooting
---------------

Common Issues
~~~~~~~~~~~~~

**Schema not found**: Ensure the schema file exists and follows the naming conventions.

**Schema not rendering**: Check that the schema file contains valid JSON.

**Performance issues**: Use ``onclick`` render mode for large schemas or many schemas on one page.

**Layout issues**: Adjust ``direction``, ``height``, and ``width`` options to fit your content better.
