======================================
autodoc Cheatsheet
======================================

**Activate autodoc in conf.py:**

.. code-block:: python

    extensions = [
        ...
        'sphinx.ext.autodoc',
    ]

**Ensure Code Can Be Imported:**

.. code-block:: python

    sys.path.insert(0, os.path.abspath('../src'))
    autodoc_mock_imports = ["missing_dependency"]

**Directives:**

.. - .. automodule:: module.name
.. - .. autoclass:: ClassName
.. - .. autoexception:: ExceptionName
.. - .. autofunction:: function_name
.. - .. autodecorator:: decorator_name
.. - .. autodata:: data_name
.. - .. automethod:: method_name
.. - .. autoattribute:: attribute_name
.. - .. autoproperty:: property_name

**Options:**

- :members: (no value or comma-separated list)
- :undoc-members:
- :private-members: (no value or comma-separated list)
- :special-members: (no value or comma-separated list)
- :inherited-members: (optional ancestor class name)
- :show-inheritance:
- :no-index:
- :imported-members:
- :exclude-members: (comma-separated list)
- :member-order: 'bysource', 'alphabetical', 'groupwise'
- :annotation: (optional value)
- :no-value:

**Configuration Values:**

- **autoclass_content**: "class", "both", "init"
- **autodoc_class_signature**: "mixed", "separated"
- **autodoc_member_order**: 'alphabetical', 'bysource', 'groupwise'
- **autodoc_default_options**: (dictionary of options)
- **autodoc_docstring_signature**: True, False
- **autodoc_mock_imports**: (list of modules)
- **autodoc_typehints**: 'signature', 'description', 'none', 'both'
- **autodoc_typehints_description_target**: 'all', 'documented', 'documented_params'
- **autodoc_type_aliases**: (dictionary of type aliases)
- **autodoc_typehints_format**: 'fully-qualified', 'short'
- **autodoc_preserve_defaults**: True, False
- **autodoc_warningiserror**: True, False
- **autodoc_inherit_docstrings**: True, False
- **suppress_warnings**: 'autodoc', 'autodoc.import_object'

**Events:**

- **autodoc-process-docstring**:
  - Parameters: app, what, name, obj, options, lines

- **autodoc-before-process-signature**:
  - Parameters: app, obj, bound_method

- **autodoc-process-signature**:
  - Parameters: app, what, name, obj, options, signature, return_annotation

- **autodoc-process-bases**:
  - Parameters: app, name, obj, options, bases

- **autodoc-skip-member**:
  - Parameters: app, what, name, obj, skip, options

**Docstring Preprocessing Functions:**

- **cut_lines(pre, post=0, what=None)**:
  - Removes the first `pre` and last `post` lines of every docstring.

- **between(marker, what=None, keepempty=False, exclude=False)**:
  - Keeps or excludes lines between lines matching `marker`.

**Examples:**

.. .. automodule:: noodle
..    :members:
..    :undoc-members:
..    :private-members: _spicy, _garlickly

.. .. autoclass:: Noodle
..    :members: eat, slurp
..    :inherited-members:
..    :show-inheritance:

.. .. autofunction:: io.open

.. .. autodata:: CD_DRIVE
..    :annotation: = your CD device name

.. .. autoproperty:: my_property
