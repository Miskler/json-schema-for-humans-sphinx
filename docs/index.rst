JSON Schema for Humans Sphinx Extension
=======================================

Welcome to the documentation for the JSON Schema for Humans Sphinx Extension.

This extension automatically integrates JSON schema documentation into your Sphinx documentation,
using the `json-schema-for-humans <https://github.com/coveooss/json-schema-for-humans>`_ library
to generate beautiful, interactive HTML representations.

.. toctree::
   :maxdepth: 2
   :caption: Getting Started:

   installation
   quickstart

.. toctree::
   :maxdepth: 2
   :caption: User Guide:

   configuration
   usage
   examples

.. toctree::
   :maxdepth: 2
   :caption: Reference:

   api
   changelog

.. toctree::
   :maxdepth: 2
   :caption: Development:

   development

Features
--------

- 🔄 **Automatic schema inclusion**: Schemas are automatically included in autodoc-generated documentation
- 📁 **Flexible file naming**: Support for multiple naming conventions
- 🎨 **Beautiful rendering**: Uses json-schema-for-humans for rich HTML output
- 🔧 **Manual inclusion**: `schema` directive for manual schema inclusion
- 🧪 **Testing support**: Fixtures for testing schema documentation
- 🌙 **Dark mode**: Support for dark theme styling
- ⚡ **Performance**: Optimized rendering with lazy loading
- 📖 **Rich documentation**: Comprehensive guides and examples

Quick Start
-----------

1. Install the extension:

.. code-block:: bash

    pip install jsoncrack-for-sphinx

2. Add to your ``conf.py``:

.. code-block:: python

    extensions = ['jsoncrack_for_sphinx']

3. Use in your documentation:

.. code-block:: rst

    .. schema:: user_schema
       :title: User Schema
       :description: Schema for user data

Getting Help
------------

- Check the :doc:`quickstart` guide for quick setup
- Read the :doc:`usage` guide for detailed examples
- Browse the :doc:`api` reference for technical details
- Report issues on `GitHub <https://github.com/miskler/json-schema-for-humans-sphinx/issues>`_

Indices and Tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
