Developer Interface
===================

.. module:: fpyutils

Main Interface
--------------

Examples for the most relevant api functions can be viewed in the test
file. fpyutils's API uses `type hints`_ instead of assertions to check 
input and output types.

.. _type hints: https://docs.python.org/3/library/typing.html

.. autofunction:: get_line_matches
.. autofunction:: insert_string_at_line
.. autofunction:: remove_line_interval

Exceptions
----------

.. autoexception:: LineOutOfFileBoundsError
.. autoexception:: NegativeLineRangeError

