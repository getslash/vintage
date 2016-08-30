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

       >>> @deprecated(message='Use new_func instead')
       ... def my_old_func(a, b, c):
       ...     return a + b +c

       >>> my_old_func(1, 2, 3)
       1: DeprecationWarning: __main__.my_old_func is deprecated. Use new_func instead
       6


You can also provide an explicit message

Table Of Contents
-----------------
       
.. toctree::
   :maxdepth: 2

   



Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

