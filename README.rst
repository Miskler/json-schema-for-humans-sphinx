stoplightio-schema-sphinx
=========================

This package provides a simple Sphinx extension that automatically adds
JSON schemas to function and method documentation. Schemas are searched in
a directory specified by ``json_schema_dir`` in your ``conf.py``.

The file naming convention is::

   <ClassName>.<method>.schema.json
   <function>.schema.json

When ``autodoc`` processes a function or method it will look for the
corresponding schema file and append it to the generated documentation.

Generating Schemas
------------------

Schema files can be produced using the `@stoplight/json-schema-generator`
package from npm. After installing Node.js and npm run::

   npx -y @stoplight/json-schema-generator --file input.json --schemadir schemas

This will place ``input.schema.json`` inside the ``schemas`` directory which the
extension can then pick up during documentation builds.

Example
-------

Add the extension and configure ``json_schema_dir`` in ``conf.py``::

   extensions = [
       "sphinx.ext.autodoc",
       "stoplightio_schema_sphinx",
   ]
   json_schema_dir = os.path.join(os.path.dirname(__file__), "schemas")

Create ``schemas/MyClass.my_method.schema.json`` and the schema will appear
in your documentation for ``MyClass.my_method``.

A ``schema_to_rst`` fixture is also provided for tests to convert schema
files to reStructuredText.
