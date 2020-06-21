Developer Interface
===================

.. module:: fpyutils

Main Interface
--------------

Examples for the most relevant api functions can be viewed in the test
file. fpyutils's API uses `type hints`_ instead of assertions to check 
input and output types.

.. _type hints: https://docs.python.org/3/library/typing.html

.. autofunction:: fpyutils.filelines.get_line_matches
.. autofunction:: fpyutils.filelines.insert_string_at_line
.. autofunction:: fpyutils.filelines.remove_line_interval
.. autofunction:: fpyutils.shell.execute_command_live_output
.. autofunction:: fpyutils.yaml.load_configuration
.. autofunction:: fpyutils.path.add_trailing_slash
.. autofunction:: fpyutils.path.gen_pseudorandom_path

Exceptions
----------

.. autoexception:: LineOutOfFileBoundsError
.. autoexception:: NegativeLineRangeError
