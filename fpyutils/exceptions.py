#

"""Exceptions file."""


class LineOutOfFileBoundsError(Exception):
    """Line out of bounds.

    Raises an exception if there was an attempt to access a non-existing line
    in a file.
    """
