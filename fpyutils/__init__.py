# Define exportable exceptions here.

"""Exposed API."""

from .filelines import (insert_string_at_line,
                        remove_line_interval,
                        get_line_matches)
from .exceptions import (LineOutOfFileBoundsError)
