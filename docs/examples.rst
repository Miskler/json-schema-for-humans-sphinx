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

These schemas demonstrate various JSON Schema features including:

- Object definitions with required and optional properties
- Array handling with item schemas
- String pattern validation
- Numeric constraints
- Nested object structures
- Conditional schema validation
