how_short
=========

Simple Decorator to measure a function execution time.
Clone of `how-long <https://pypi.org/project/how-long/>`_.

Example
_______

.. code-block:: python

    from how_long import timer


    @timer
    def some_function():
        return [x for x in range(10_000_000)]