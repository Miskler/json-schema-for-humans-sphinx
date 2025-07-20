Search Patterns Analysis
========================

This section provides a detailed analysis of how the schema search system works in JSONCrack for Sphinx Extension.

Object Structure
----------------

Let's consider an example of a full object path:

.. code-block:: text

    perekrestok_api.endpoints.catalog.ProductService.similar
    │              │         │       │              │
    │              └─────────┼───────┘              │
    │                        │                      │
    Package                 Path                   Class.Method

Path components:

* **Package**: ``perekrestok_api``
* **Path components**: ``endpoints.catalog``
* **Class**: ``ProductService``
* **Method**: ``similar``
* **Full path**: ``perekrestok_api.endpoints.catalog.ProductService.similar``

All Possible SearchPolicy Combinations
---------------------------------------

1. Default Policy
~~~~~~~~~~~~~~~~~

.. code-block:: python

    SearchPolicy(
        include_package_name=False,  # default
        include_path_to_file=True,   # default
        path_to_file_separator=PathSeparator.DOT,
        path_to_class_separator=PathSeparator.DOT
    )

**Search patterns (in priority order):**

.. code-block:: text

    1. ProductService.similar.schema.json ← Highest priority
    2. ProductService.similar.json
    3. catalog.ProductService.similar.schema.json
    4. catalog.ProductService.similar.json
    5. endpoints.catalog.ProductService.similar.schema.json
    6. endpoints.catalog.ProductService.similar.json
    7. similar.schema.json
    8. similar.json
    9. perekrestok_api.endpoints.catalog.ProductService.similar.schema.json ← Fallback
    10. perekrestok_api.endpoints.catalog.ProductService.similar.json

2. Without Intermediate Paths
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    SearchPolicy(
        include_package_name=False,
        include_path_to_file=False,  # ❌ Remove endpoints.catalog
        path_to_file_separator=PathSeparator.DOT,
        path_to_class_separator=PathSeparator.DOT
    )

**Search patterns:**

.. code-block:: text

    1. ProductService.similar.schema.json ← Highest priority
    2. ProductService.similar.json
    3. similar.schema.json
    4. similar.json
    5. perekrestok_api.endpoints.catalog.ProductService.similar.schema.json ← Fallback
    6. perekrestok_api.endpoints.catalog.ProductService.similar.json

**🚫 Skipped:**

* ``catalog.ProductService.similar.schema.json``
* ``endpoints.catalog.ProductService.similar.schema.json``

3. With Package Name Included
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    SearchPolicy(
        include_package_name=True,   # ✅ Include perekrestok_api
        include_path_to_file=True,
        path_to_file_separator=PathSeparator.DOT,
        path_to_class_separator=PathSeparator.DOT
    )

**Search patterns:**

.. code-block:: text

    1. ProductService.similar.schema.json ← Highest priority
    2. ProductService.similar.json
    3. catalog.ProductService.similar.schema.json
    4. catalog.ProductService.similar.json
    5. endpoints.catalog.ProductService.similar.schema.json
    6. endpoints.catalog.ProductService.similar.json
    7. perekrestok_api.endpoints.catalog.ProductService.similar.schema.json ← Included earlier
    8. perekrestok_api.endpoints.catalog.ProductService.similar.json
    9. similar.schema.json
    10. similar.json

4. Slash Separators
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    SearchPolicy(
        include_package_name=False,
        include_path_to_file=True,
        path_to_file_separator=PathSeparator.SLASH,  # 🔄 Use /
        path_to_class_separator=PathSeparator.DOT
    )

**Search patterns:**

.. code-block:: text

    1. ProductService.similar.schema.json ← Highest priority
    2. ProductService.similar.json
    3. endpoints/catalog/ProductService.similar.schema.json ← Directories
    4. endpoints/catalog/ProductService.similar.json
    5. similar.schema.json
    6. similar.json
    7. perekrestok_api.endpoints.catalog.ProductService.similar.schema.json ← Fallback
    8. perekrestok_api.endpoints.catalog.ProductService.similar.json

5. Slashes + Package
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    SearchPolicy(
        include_package_name=True,   # ✅ Include perekrestok_api
        include_path_to_file=True,
        path_to_file_separator=PathSeparator.SLASH,
        path_to_class_separator=PathSeparator.DOT
    )

**Search patterns:**

.. code-block:: text

    1. ProductService.similar.schema.json ← Highest priority
    2. ProductService.similar.json
    3. endpoints/catalog/ProductService.similar.schema.json
    4. endpoints/catalog/ProductService.similar.json
    5. perekrestok_api/endpoints/catalog/ProductService.similar.schema.json ← Full structure
    6. perekrestok_api/endpoints/catalog/ProductService.similar.json
    7. similar.schema.json
    8. similar.json

6. No Separators
~~~~~~~~~~~~~~~~

.. code-block:: python

    SearchPolicy(
        include_package_name=False,
        include_path_to_file=True,
        path_to_file_separator=PathSeparator.NONE,  # 🔄 No separators
        path_to_class_separator=PathSeparator.NONE
    )

**Search patterns:**

.. code-block:: text

    1. ProductServicesimilar.schema.json ← Concatenated
    2. ProductServicesimilar.json
    3. catalogProductServicesimilar.schema.json
    4. catalogProductServicesimilar.json
    5. endpointscatalogProductServicesimilar.schema.json
    6. endpointscatalogProductServicesimilar.json
    7. similar.schema.json
    8. similar.json
    9. perekrestok_api.endpoints.catalog.ProductService.similar.schema.json ← Fallback
    10. perekrestok_api.endpoints.catalog.ProductService.similar.json

7. Extreme Configuration
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    SearchPolicy(
        include_package_name=True,
        include_path_to_file=False,  # ❌ No intermediate paths
        path_to_file_separator=PathSeparator.SLASH,
        path_to_class_separator=PathSeparator.NONE
    )

**Search patterns:**

.. code-block:: text

    1. ProductServicesimilar.schema.json ← Concatenated class+method
    2. ProductServicesimilar.json
    3. perekrestok_api/ProductServicesimilar.schema.json ← Package + concatenated
    4. perekrestok_api/ProductServicesimilar.json
    5. similar.schema.json
    6. similar.json
    7. perekrestok_api.endpoints.catalog.ProductService.similar.schema.json ← Fallback
    8. perekrestok_api.endpoints.catalog.ProductService.similar.json

8. With Custom Patterns
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    SearchPolicy(
        include_package_name=False,
        include_path_to_file=True,
        path_to_file_separator=PathSeparator.DOT,
        path_to_class_separator=PathSeparator.DOT,
        custom_patterns=[
            'api_{class_name}_{method_name}',
            '{object_name}_spec',
            'schemas/{class_name}/{method_name}'
        ]
    )

**Search patterns:**

.. code-block:: text

    1. api_ProductService_similar.schema.json ← Custom 1
    2. api_ProductService_similar.json
    3. perekrestok_api.endpoints.catalog.ProductService.similar_spec.schema.json ← Custom 2
    4. perekrestok_api.endpoints.catalog.ProductService.similar_spec.json
    5. schemas/ProductService/similar.schema.json ← Custom 3
    6. schemas/ProductService/similar.json
    7. ProductService.similar.schema.json ← Standard patterns
    8. ProductService.similar.json
    9. catalog.ProductService.similar.schema.json
    10. catalog.ProductService.similar.json
    11. endpoints.catalog.ProductService.similar.schema.json
    12. endpoints.catalog.ProductService.similar.json
    13. similar.schema.json
    14. similar.json
    15. perekrestok_api.endpoints.catalog.ProductService.similar.schema.json
    16. perekrestok_api.endpoints.catalog.ProductService.similar.json

Summary Table of Combinations
------------------------------

.. list-table::
   :header-rows: 1
   :widths: 15 15 10 10 30 30

   * - include_package
     - include_path
     - file_sep
     - class_sep
     - First Pattern
     - Intermediate
   * - False
     - True
     - DOT
     - DOT
     - ``ProductService.similar``
     - ``catalog.ProductService.similar``\\
       ``endpoints.catalog.ProductService.similar``
   * - False
     - False
     - DOT
     - DOT
     - ``ProductService.similar``
     - 🚫 Skipped
   * - True
     - True
     - DOT
     - DOT
     - ``ProductService.similar``
     - Full package prioritized
   * - False
     - True
     - SLASH
     - DOT
     - ``ProductService.similar``
     - ``endpoints/catalog/ProductService.similar``
   * - True
     - True
     - SLASH
     - DOT
     - ``ProductService.similar``
     - ``perekrestok_api/endpoints/catalog/ProductService.similar``
   * - False
     - True
     - NONE
     - NONE
     - ``ProductServicesimilar``
     - ``catalogProductServicesimilar``\\
       ``endpointscatalogProductServicesimilar``
   * - True
     - False
     - SLASH
     - NONE
     - ``ProductServicesimilar``
     - ``perekrestok_api/ProductServicesimilar``

Usage Recommendations
----------------------

For Simple Schema Organization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    SearchPolicy(include_path_to_file=False)

**Searches for:** ``ProductService.similar.schema.json``, ``similar.schema.json``

For Hierarchical Organization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    SearchPolicy(
        include_path_to_file=True,
        path_to_file_separator=PathSeparator.SLASH
    )

**Searches for:** ``endpoints/catalog/ProductService.similar.schema.json``

For API-Specific Schemas
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    SearchPolicy(
        custom_patterns=['api_{class_name}_{method_name}']
    )

**Searches for:** ``api_ProductService_similar.schema.json``

For Maximum Flexibility
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    SearchPolicy(
        include_package_name=True,
        include_path_to_file=True,
        path_to_file_separator=PathSeparator.SLASH,
        custom_patterns=['api_{class_name}_{method_name}']
    )

**Searches for all possible combinations!**

Practical Examples
------------------

Example 1: Simple Project Structure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you have a simple project structure and want to keep schemas close to code:

.. code-block:: python

    # conf.py
    jsoncrack_default_options = {
        'search_policy': SearchPolicy(
            include_package_name=False,
            include_path_to_file=False
        )
    }

This will search for schemas in this order:

.. code-block:: text

    MyClass.method.schema.json
    method.schema.json

Example 2: Centralized Schemas
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If all schemas are stored in a separate ``schemas/`` directory:

.. code-block:: python

    # conf.py
    json_schema_dir = 'schemas'
    jsoncrack_default_options = {
        'search_policy': SearchPolicy(
            include_package_name=True,
            include_path_to_file=True,
            path_to_file_separator=PathSeparator.SLASH
        )
    }

File structure:

.. code-block:: text

    schemas/
    ├── mypackage/
    │   └── module/
    │       └── MyClass.method.schema.json
    └── MyClass.method.schema.json

Example 3: API Documentation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For REST API with custom schema names:

.. code-block:: python

    # conf.py
    jsoncrack_default_options = {
        'search_policy': SearchPolicy(
            custom_patterns=[
                'api_{class_name}_{method_name}.request.json',
                'api_{class_name}_{method_name}.response.json',
                '{class_name}_{method_name}_schema.json'
            ]
        )
    }

Will search for:

.. code-block:: text

    api_UserService_create.request.json
    api_UserService_create.response.json
    UserService_create_schema.json

Schema Search Debugging
-----------------------

To debug schema search functionality, enable detailed logging:

.. code-block:: python

    # conf.py
    jsoncrack_debug_logging = True

This will output detailed information about:

* Generated search patterns
* Found and not found files
* Reasons for selecting specific schemas
* Errors during schema processing

Example debug output:

.. code-block:: text

    [JSONCrack] Searching for schema: mypackage.module.MyClass.method
    [JSONCrack] Generated patterns:
      1. MyClass.method.schema.json
      2. MyClass.method.json
      3. module.MyClass.method.schema.json
      4. method.schema.json
    [JSONCrack] Found: schemas/MyClass.method.schema.json
    [JSONCrack] Selected schema: schemas/MyClass.method.schema.json
