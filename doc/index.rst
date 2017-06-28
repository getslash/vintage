Vintage
=======

Overview
--------

Vintage is a library to help you manage code deprecation cycles. It provides a decorator, ``deprecated``, which marks functions and methods as deprecated

Usage
-----

Decorate your functions with ``deprecated``, optionally providing a message:

.. code-block:: python

       >>> from vintage import deprecated
       
       >>> @deprecated
       ... def my_old_func(a, b, c):
       ...     return a + b +c

       >>> my_old_func(1, 2, 3)
       1: DeprecationWarning: __main__.my_old_func is deprecated.
       6

You can also provide an explicit message:

.. code-block:: python
       
       >>> @deprecated(message='Use new_func instead')
       ... def my_old_func(a, b, c):
       ...     return a + b +c

       >>> my_old_func(1, 2, 3)
       1: DeprecationWarning: __main__.my_old_func is deprecated. Use new_func instead
       6


Deprecations can also be emitted by using a dedicated function:

.. code-block:: python
       
       >>> vintage.warn_deprecation('use other thing')

Suppressing Deprecations
------------------------

Vintage allows suppressing deprecations through the ``get_no_deprecations_context`` context:

.. code-block:: python
       
       >>> with vintage.get_no_deprecations_context():
       ...     # deprecated code here

.. note:: The above context *does not* meddle with Python's warning mechanism, but rather suppresses Vintage deprecations only. This is useful as it does not interfere with current warning settings and/or capturing contexts. However, it means that other pieces of code emitting deprecation warnings directly would not get suppressed

Table Of Contents
-----------------
       
.. toctree::
   :maxdepth: 2

   changelog



Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

